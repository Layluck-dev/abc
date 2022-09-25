
from ..pool.pool import Pool
from ..block.block import Block
from flask import jsonify, make_response

class Chain:
    def __init__(self, blockchain:list = []) -> None:
        self.chain = blockchain
    
    def generate(self, transaction:dict) -> int:
        # self.reset()
        initialBlock = Block(1, transaction).generateBlock(self.chain)
        self.chain.append(initialBlock)
        
        return self.chain
    
    def getMostValuable(self, transactions:list) -> dict:
        latestTransaction       = transactions[-1]
        mostValuedTransaction   = None
        
        for t in transactions:
            if(t["amount"] > latestTransaction["amount"]):
                mostValuedTransaction = t
        
        return mostValuedTransaction
    
    def appendBlock(self, pool:Pool) -> int:
        if not pool.list:
            return make_response(jsonify({"info":"There are no current transactions", "status":"500"}), 500)
        
        transaction = self.getMostValuable(pool)
        pool.list.remove(transaction)
        
        if not self.chain:
            return self.generate(transaction)
        
        priorBlock = self.chain[-1]
        
        initialBlock = Block(priorBlock["index"]+1, transaction, priorBlock["currentHash"]).generateBlock(self.chain)
        self.chain.append(initialBlock)
        
        return self.chain
        
    def nuke(self):
        self.chain = []
        return make_response(jsonify({"info":"and so ends this thread...", "status":"200"}),200)
        