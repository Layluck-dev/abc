
import hashlib
from typing import Tuple
import uuid

from ..types import TransActionOutput, TransactionData

class TransActionInput:
    def validateBalance(self, balance: float, amount: float) -> float:
        return balance-amount
    
    def generateKey(self, balance: float, amount: float, isRemainder: bool) -> str:
        return hashlib.sha256(bytes(f"{balance}{str(isRemainder)}{amount}", 'utf-8')).hexdigest()
    
    def generateOutputs(self, transaction: TransactionData, balance:float) -> Tuple[TransActionOutput, TransActionOutput] | None:
        remainder = self.validateBalance(balance, transaction["amount"])
        
        if remainder < 0:
            return None
        
        commonId = str(uuid.uuid4())
        
        outputTransaction: TransActionOutput = {
            "timestamp":    transaction["timestamp"],
            "previousHash": transaction["inputHash"],
            "id":           commonId,
            "hash":         self.generateKey(balance, transaction["amount"], False),
            "amount":       transaction["amount"],
            "receiverID":   transaction["receiverID"],
            "isRemainder":  False
        }
        
        outputRemainder: TransActionOutput = {
            "timestamp":    transaction["timestamp"],
            "previousHash": transaction["inputHash"],
            "id":           commonId,
            "hash":         self.generateKey(balance, transaction["amount"], True),
            "amount":       remainder,
            "receiverID":   transaction["receiverID"],
            "isRemainder":  True
        }
        
        return (outputTransaction, outputRemainder)