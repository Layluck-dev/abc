
from datetime import datetime
import hashlib
import json

from ..types import BlockData, TransactionData

class Block:
    def __init__(self, index:int, transaction:TransactionData, priorBlockHash:str = "initial") -> None:
        self.index          = index
        self.transaction    = transaction
        self.priorBlockHash = priorBlockHash
        self.timestamp      = datetime.now()
        
    
    def generateBlock(self, block:BlockData | None) -> BlockData:
        priorBlock:BlockData = {}
        
        if not block:
            priorBlock["proof"] = 0
        else:
            priorBlock = block
            
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
    
    def proofOfWork(self, priorBlock:BlockData) -> int:
        currentProof:int = 0
        
        while self.validate(priorBlock, currentProof) is False:
            currentProof += 1

        return currentProof

    def validate(self, priorBlock:BlockData, currentProof:int) -> bool:
        attemp = (str(priorBlock["proof"])+str(currentProof)+str(self.timestamp)).encode()
        hashedAttemp = hashlib.sha256(attemp).hexdigest()
        return hashedAttemp[:5] == "00000"