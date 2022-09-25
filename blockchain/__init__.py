from flask import Flask, request
from .chain.chain import Chain
from .pool.pool import Pool

def create_app(test_config=None):
    server = Flask(__name__)
    chain = Chain()
    pool = Pool()
    transaction = None
    baseUrl = "/api/"
    
    @server.post(baseUrl + 'transaction/new')
    def createTransaction():
        return None

    @server.get(baseUrl + 'pool/index')
    def getPool():
        return None
    
    @server.get(baseUrl + 'block/new')
    def generateBlock():
        return Chain.appendBlock(chain, pool)

    return server