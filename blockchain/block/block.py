
from datetime import datetime
import hashlib
import json
from typing import Dict, TypedDict

blockHash_type = None | str

class Transaction(TypedDict):
    sender: int
    receiver: int
    amount: float

class BlockData(TypedDict):
    index:        int
    timestamp:    datetime
    proof:        None
    priorHash:    str
    currentHash:  str
    transaction:  Transaction


class Block:
    def __init__(self, index:int, transaction:Transaction, priorBlockHash:None | str = None) -> None:
        self.index          = index
        self.transaction    = transaction
        self.priorBlockHash = priorBlockHash
        self.timestamp      = datetime.now()
        
    
    def generateBlock(self, blockchain) -> BlockData:
        priorBlock:dict = {}
        
        if not blockchain:
            priorBlock["proof"] = 0
        else:
            priorBlock = blockchain[-1]
            
        return {
            "index":        self.index,
            "timestamp":    datetime.now(),
            "proof":        None,
            "priorHash":    self.priorBlockHash,
            "currentHash":  None,
            "transaction":  self.transaction
        }
    
    def generateHash(self) -> str:
        blockData = json.dumps(str(self.index) + str(self.timestamp) + self.priorBlockHash + json.dumps(self.transaction, sort_keys=True, indent=4, default=str)).encode("utf-8")
        return hashlib.sha256(blockData).hexdigest()
    
    def proofOfWork(self, priorBlock) -> int:
        priorProof  = priorBlock['proof']
        timestamp   = self.timestamp

        proof = 0
        # TODO check proof of work
        return proof