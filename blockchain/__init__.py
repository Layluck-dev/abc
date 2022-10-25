from email.mime import base
from flask import Flask, request, jsonify, make_response

from blockchain.pool.transactionPool import TransactionPool

from .chain.validation import ChainValidation
from .transaction.transaction import Transaction
from .chain.chain import Chain
from .pool.pool import Pool

def create_app(test_config=None):
    server              = Flask(__name__)
    chain               = Chain()
    pool                = Pool()
    transactionOutputs  = TransactionPool()
    transaction         = Transaction(pool, transactionOutputs)
    baseUrl             = "/api/"
    
    @server.get(baseUrl + 'pool/poll')
    def pollPool():
        return make_response(jsonify(pool.list), 200)
    
    @server.post(baseUrl + 'transaction/new')
    def createTransaction():
        return transaction.createTransaction(request.json)
    
    @server.get(baseUrl + 'block/new')
    def generateBlock():
        return chain.appendBlock(chain, pool)
    
    @server.get(baseUrl + 'blockchain/nuke')
    def nukeChain():
        return chain.nuke()
    
    @server.get(baseUrl + 'blockchain/poll')
    def pollChain():
        return make_response(jsonify(chain.chain), 200)
    
    @server.get(baseUrl + 'blockchain/validate')
    def validateChain():
        return ChainValidation().validate(chain)
    
    @server.get(baseUrl + 'transactionOutputs/poll')
    def pollTransactionOutputs():
        return transactionOutputs.pollPool()
    
    @server.put(baseUrl + 'transactionOutputs/poll')
    def pollTransactionOutput():
        return transactionOutputs.pollOutput(request.json)
    
    @server.get(baseUrl + 'blockchain/length')
    def getChainlength():
        return chain.getHeight()

    return server