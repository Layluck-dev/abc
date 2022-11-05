from email.mime import base
from flask import Flask, request, jsonify, make_response

from .nodes.register import NodeRegistry

from .pool.transactionPool import TransactionPool

from .chain.validation import ChainValidation
from .transaction.transaction import Transaction
from .chain.chain import Chain
from .pool.pool import Pool

def create_app(test_config=None):
    server              = Flask(__name__)
    pool                = Pool()
    transactionOutputs  = TransactionPool()
    nodeRegistry        = NodeRegistry()
    chain               = Chain(transactionOutputs, nodeRegistry)
    transaction         = Transaction(pool, transactionOutputs, chain)
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
    
    @server.get(baseUrl + 'openRemainder')
    def getOpenRemainder():
        return transactionOutputs.getOpenRemainder(request.json)
    
    @server.get(baseUrl + 'blockchain/length')
    def getChainlength():
        return chain.getLength()

    @server.get(baseUrl + 'balance')
    def getBalance():
        return chain.getBalanceByUid(request.json)
    
    @server.get(baseUrl + 'consensus')
    def getGetChainValidation():
        return ChainValidation().getValidation(chain, request.json)
    
    @server.post(baseUrl + 'assert')
    def incomingChain():
        isValid = ChainValidation().getValidation(chain, request.json).ok
        
        if not isValid:
            return make_response(jsonify({"info":"chain could not be validated","status":400}),400)
        
        return make_response(jsonify({"info":"chain successfully consolidated","status":200}),200)
        
    
    return server