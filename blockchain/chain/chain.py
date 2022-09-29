
from ..types import TransactionData
from ..pool.pool import Pool
from ..block.block import Block, BlockData
from flask import jsonify, make_response, Response

class Chain:
    def __init__(self, blockchain:list[BlockData] = []) -> None:
        self.chain = blockchain
    
    def generate(self, transaction:TransactionData) -> list[BlockData]:
        lastBlock:BlockData | None = None
        if len(self.chain) > 0:
            lastBlock = self.chain[-1]

        initialBlock = Block(1, transaction).generateBlock(lastBlock)
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
            return make_response(jsonify({"info":"There are no current transactions", "status":"500"}), 500)
        
        transaction = self.getMostValuable(pool.list)
        pool.list.remove(transaction)
        
        if not self.chain:
            return make_response(jsonify(self.generate(transaction)), 200)
        
        priorBlock      = self.chain[-1]
        initialBlock    = Block(priorBlock["index"]+1, transaction, priorBlock["currentHash"]).generateBlock(priorBlock)
        self.chain.append(initialBlock)
        
        return make_response(jsonify(self.chain), 200)
        
    def nuke(self) -> Response:
        self.chain.clear()
        return make_response(jsonify({"info":"and so ends this thread...", "status":"200"}),200)
    