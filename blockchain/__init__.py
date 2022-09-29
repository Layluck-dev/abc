from flask import Flask, request, jsonify, make_response

from .chain.validation import ChainValidation
from .transaction.transaction import Transaction
from .chain.chain import Chain
from .pool.pool import Pool

def create_app(test_config=None):
    server          = Flask(__name__)
    chain           = Chain()
    pool            = Pool()
    transaction     = Transaction(pool)
    baseUrl         = "/api/"
    
    @server.get(baseUrl + 'pool/poll')
    def pollPool():
        return make_response(jsonify(pool.list), 200)
    
    @server.post(baseUrl + 'transaction/new')
    def createTransaction():
        return transaction.createTransaction(request.json)
    
    @server.get(baseUrl + 'block/new')
    def generateBlock():
        return Chain.appendBlock(chain, pool)
    
    @server.get(baseUrl + 'blockchain/nuke')
    def nukeChain():
        return Chain.nuke()
    
    @server.get(baseUrl + 'blockchain/poll')
    def pollChain():
        return make_response(jsonify(chain.chain), 200)
    
    @server.get(baseUrl + 'blockchain/validate')
    def validateChain():
        return ChainValidation().validate(chain)

    return server