
import hashlib
import time
from ..pool.transactionPool import TransactionPool
from ..transaction.alphaHelper import AlphaTransaction

from ..types import BlockData, TransactionData

class Block:
    def __init__(self, index:int, transaction:TransactionData, priorBlockHash:str = "initial") -> None:
        self.index:int                   = index
        self.timestamp:float             = time.time()
        self.proof:int                   = 0
        self.priorBlockHash:str          = priorBlockHash
        self.currentHash:str             = ""
        self.transaction:TransactionData = transaction
        
    
    def generateBlock(self, transactionPool:TransactionPool, priorBlock:BlockData | None = None) -> BlockData:

        if not priorBlock:
            input = AlphaTransaction()
            alphaTransaction = input.getAlphaTransaction()
            
            transactionPool.appendTransactions(alphaTransaction["transactionOutput"])
            
            return {
                "index":        self.index,
                "timestamp":    self.timestamp,
                "proof":        0,
                "priorHash":    "AlphaBlock",
                "currentHash":  self.generateHash(),
                "transaction":  alphaTransaction
            }
        
        self.proof = self.proofOfWork(priorBlock["proof"])
        
        return {
            "index":        self.index,
            "timestamp":    self.timestamp,
            "proof":        self.proof,
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
        return hashlib.sha256(bytes(self.__str__(), 'utf-8')).hexdigest()
    
    def proofOfWork(self, priorProof:int) -> int:
        currentProof:int = 0
        
        while self.validate(priorProof, currentProof) is False:
            currentProof += 1

        return currentProof

    def validate(self, priorProof:int, currentProof:int, timestamp:float|None = None) -> bool:
        time = self.timestamp
        if timestamp is not None:
            time = timestamp
        
        attemp = (str(priorProof)+str(currentProof)+str(time)).encode()
        hashedAttemp = hashlib.sha256(attemp).hexdigest()
        return hashedAttemp[:5] == "00000"
    
    #omits current hash since this function is used to generate the current hash
    def __str__(self) -> str:
        return f"index: {self.index}, timestamp: {self.timestamp}, proof: {self.proof}, priorHash: {self.priorBlockHash}, transaction: ( timestamp: {self.transaction['timestamp']}, senderID: {self.transaction['senderID']}, receiverID: {self.transaction['receiverID']}, amount: {self.transaction['amount']})"