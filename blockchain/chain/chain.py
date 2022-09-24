from ..block.block import Block

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
    
    def appendBlock(self, pool:list) -> int:
        # TODO check pool
        
        transaction = self.getMostValuable(pool)
        #TODO remove from pool
        
        if not self.chain:
            return self.generate(transaction)
        
        priorBlock = self.chain[-1]
        
        initialBlock = Block(priorBlock["index"]+1, transaction, priorBlock["currentHash"]).generateBlock(self.chain)
        self.chain.append(initialBlock)
        
        return self.chain
        
    def nuke(self):
        self.chain = []
        