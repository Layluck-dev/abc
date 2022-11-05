
import json
from typing import Any
from ..nodes.register import NodeRegistry

from ..nodes.requestHandler import RequestHandler
from ..pool.transactionPool import TransactionPool
from ..types import TransActionOutput, TransactionData
from ..pool.pool import Pool
from ..block.block import Block, BlockData
from flask import jsonify, make_response, Response

class Chain:
    def __init__(self, transactionPool: TransactionPool, nodeRegister:NodeRegistry) -> None:
        self.chain:list[BlockData] = []
        self.newChain:list[BlockData] = []
        self.nodes = nodeRegister
        self.transactionPool = transactionPool
    
    def generate(self, transaction:TransactionData) -> list[BlockData]:
        lastBlock:BlockData | None = None
        if len(self.chain) > 0:
            lastBlock = self.chain[-1]

        initialBlock = Block(1, transaction).generateBlock(self.transactionPool, lastBlock)
        self.chain.append(initialBlock)
        
        return self.chain
    
    def getMostValuable(self, transactions:list) -> TransactionData:
        latestTransaction       = transactions[-1]
        mostValuedTransaction   = latestTransaction
        
        for t in transactions:
            if(t["amount"] > latestTransaction["amount"]):
                mostValuedTransaction = t
        
        return mostValuedTransaction
    
    def appendBlock(self, pool:Pool) -> Response:
        if not pool.list:
            return make_response(jsonify({"info":"There are no current transactions", "status":"404"}), 404)
        
        transaction = self.getMostValuable(pool.list)
        pool.list.remove(transaction)
        
        if not self.chain:
            return make_response(jsonify(self.generate(transaction)), 200)
        
        priorBlock      = self.chain[-1]
        currentBlock    = Block(priorBlock["index"]+1, transaction, priorBlock["currentHash"]).generateBlock(self.transactionPool, priorBlock)
        
        self.newChain = self.chain
        self.newChain.append(currentBlock)
        
        requestHandler = RequestHandler(self.nodes)
        if requestHandler.validateChain(self.chain):
            self.chain.append(currentBlock)
            return make_response(jsonify(self.chain), 200)
        
        return make_response(jsonify({"info":"could not validate chain","status":500}), 500)
        
        
    def nuke(self) -> Response:
        self.chain.clear()
        return make_response(jsonify({"info":"and so ends this thread...", "status":"200"}),200)
    
    def getLength(self) -> Response:
        return make_response(jsonify({"info":len(self.chain)}), 200)
    
    def balanceByTransactionOutput(self, transactionOutput:TransActionOutput) -> float:
        result:float = transactionOutput["amount"]
        
        for block in self.chain:
            if transactionOutput["timestamp"] < block["transaction"]["timestamp"]:
                break
            
            if transactionOutput["receiverID"] == block["transaction"]["receiverID"]:
                result = result + block["transaction"]["amount"]
                
        return result
    
    def balanceByUid(self, userID:int) -> float | None:
        transactionRemainder = self.transactionPool.openRemainderByUid(userID)
        if not transactionRemainder:
            return None
        return self.balanceByTransactionOutput(transactionRemainder)
    
    def getBalanceByUid(self, balanceReq:Any):
        try:
            userID:int = int(balanceReq["userID"])
        except:
            return make_response(jsonify({"info":"malformed request", "status":"400"}), 400)
        
        balance = self.balanceByUid(userID)
        if not balance:
            return make_response(jsonify({"info":"no transaction history found for this user", "status":"404"}), 404)
        
        return make_response(jsonify({"balance":balance}), 200)
    
    def consolidate(self, incomingChain:Any)->Response:
        try:
            incomingChain = json.loads(incomingChain)
            currentChain = json.dumps(self.chain)
            
            if incomingChain == currentChain:
                return make_response(jsonify({"info":"chain already in sync"}), 200)
            
            tempChain = self
            tempChain.chain = incomingChain
            checker = RequestHandler(self.nodes)
            if checker.validateChain(tempChain.chain):
                self.chain = tempChain.chain
                return make_response(jsonify({"info":"chain succesfully consolidated"}), 200)
            
            return make_response(jsonify({"info":"could not consolidate chain", "status":500}), 500)
        except:
            return make_response(jsonify({"info":"could not handle request", "status":500}), 500)