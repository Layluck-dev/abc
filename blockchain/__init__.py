from flask import Flask, request

from .transaction.transaction import Transaction
from .chain.chain import Chain
from .pool.pool import Pool

from flask import jsonify, make_response

def create_app(test_config=None):
    server = Flask(__name__)
    chain = Chain()
    pool = Pool()
    transaction = Transaction(pool)
    baseUrl = "/api/"
    
    @server.get(baseUrl + 'pool/poll')
    def pollPool():
        return make_response(jsonify(pool.list), 200)
    
    @server.post(baseUrl + 'transaction/new')
    def createTransaction():
        return transaction.createTransaction(request.json)
    
    @server.get(baseUrl + 'block/new')
    def generateBlock():
        return Chain.appendBlock(chain, pool)

    return server