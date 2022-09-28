
from datetime import datetime
import hashlib
import json
from typing import TypedDict

blockHash_type = None | str

class Transaction(TypedDict):
    sender: int
    receiver: int
    amount: float

class BlockData(TypedDict):
    index:        int
    timestamp:    datetime
    proof:        str
    priorHash:    str
    currentHash:  str
    transaction:  Transaction


class Block:
    def __init__(self, index:int, transaction:Transaction, priorBlockHash:str = "initial") -> None:
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
            "proof":        self.proofOfWork(priorBlock),
            "priorHash":    self.priorBlockHash,
            "currentHash":  self.generateHash(),
            "transaction":  self.transaction
        }
    
    def generateHash(self) -> str:
        blockData = json.dumps(str(self.index) + str(self.timestamp) + self.priorBlockHash + json.dumps(self.transaction, sort_keys=True, indent=4, default=str)).encode("utf-8")
        return hashlib.sha256(blockData).hexdigest()
    
    def proofOfWork(self, priorBlock) -> int:
        currentProof = 0
        
        while self.validate(priorBlock, currentProof) is False:
            currentProof += 1

        return currentProof

    def validate(self, priorBlock, currentProof:int) -> bool:
        attemp = (priorBlock["proof"]+currentProof+str(self.timestamp)).encode()
        hashedAttemp = hashlib.sha256(attemp).hexdigest()
        return hashedAttemp[:4] == "0000"