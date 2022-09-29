
from datetime import datetime
import hashlib
import json

from ..types import BlockData, TransactionData

class Block:
    def __init__(self, index:int, transaction:TransactionData, priorBlockHash:str = "initial") -> None:
        self.index          = index
        self.timestamp      = datetime.now()
        self.proof          = 0
        self.priorBlockHash = priorBlockHash
        self.currentHash    = ""
        self.transaction    = transaction
        
    
    def generateBlock(self, priorBlock:BlockData | None) -> BlockData:
        tempProof:int = 0
        
        if priorBlock:
            tempProof = priorBlock["proof"]
            
        return {
            "index":        self.index,
            "timestamp":    datetime.now(),
            "proof":        self.proofOfWork(tempProof),
            "priorHash":    self.priorBlockHash,
            "currentHash":  self.generateHash(),
            "transaction":  self.transaction
        }
        
    def rehydrate(self, blockData:BlockData) -> None:
        self.index          = blockData["index"]
        self.timestamp      = blockData["timestamp"]
        self.proof          = blockData["proof"]
        self.priorBlockHash = blockData["priorHash"]
        self.currentHash    = blockData["currentHash"]
        self.transaction    = blockData["transaction"]
    
    def generateHash(self) -> str:
        blockData = json.dumps(str(self.index) + str(self.timestamp) + self.priorBlockHash + json.dumps(self.transaction, sort_keys=True, indent=4, default=str)).encode("utf-8")
        return hashlib.sha256(blockData).hexdigest()
    
    def proofOfWork(self, priorProof:int) -> int:
        currentProof:int = 0
        
        while self.validate(priorProof, currentProof) is False:
            currentProof += 1

        return currentProof

    def validate(self, priorProof:int, currentProof:int, timestamp:datetime|None = None) -> bool:
        time = self.timestamp
        if timestamp is not None:
            time = timestamp
        
        attemp = (str(priorProof)+str(currentProof)+str(time)).encode()
        hashedAttemp = hashlib.sha256(attemp).hexdigest()
        return hashedAttemp[:5] == "00000"