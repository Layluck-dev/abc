
import time
from flask import jsonify, make_response, Response

from ..types import BlockData, TransactionData
from ..chain.chain import Chain
from ..block.block import Block

class ChainValidation():
    def __init__(self) -> None:
        mockTransaction:TransactionData = {"timestamp":time.time(), "senderID":0, "receiverID":0, "amount":0, "balance":0, "transactionOutput": None}
        self.block:Block                = Block(0, mockTransaction)
    
    def validate(self, blockchain:Chain) -> Response:
        if not blockchain.chain:
            return make_response(jsonify({"info":"There is no blockchain currently...", "status":"404"}), 404)
        
        for i in range(len(blockchain.chain)):
            blockData:BlockData      = blockchain.chain[i]
            priorBlockData:BlockData = blockData
            
            if i > 0:
                priorBlockData = blockchain.chain[i-1]
            
            self.block.rehydrate(blockData)
            
            if not self.hashValidation():
                return make_response(jsonify({"info":"invalid block hash", "status":"500"}), 500)

            if blockData["index"] == 1 and not self.proofValidation(0, blockData["proof"], blockData["timestamp"]):
                return make_response(jsonify({"info":"invalid block proof", "status":"500"}), 500)
            
            if blockData["index"] > 1 and not self.proofValidation(priorBlockData["proof"], blockData["proof"], blockData["timestamp"]):
                return make_response(jsonify({"info":"invalid block proof", "status":"500"}), 500)
            
            if blockData["index"] > 1 and not self.hashComparison(blockData["priorHash"], priorBlockData["currentHash"]):
                return make_response(jsonify({"info":"hash mismatch", "status":"500"}), 500)

        return make_response(jsonify(blockchain.chain), 200)
    
    def hashValidation(self) -> bool:
        return self.block.currentHash == self.block.generateHash()
    
    def proofValidation(self, priorProof:int, currentProof:int, timeStamp:float) -> bool:
        return self.block.validate(priorProof, currentProof, timeStamp)
    
    def hashComparison(self, currentBlockのpriorHash:str, priorBlockHash:str) -> bool:
        return currentBlockのpriorHash == priorBlockHash