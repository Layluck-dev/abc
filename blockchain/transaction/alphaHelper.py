import hashlib
import time
from .input import TransActionInput
from ..types import TransactionData

# mypy: ignore-errors
from ecdsa import SigningKey, NIST521p

class AlphaTransaction:
    def __init__(self) -> None:
        self.privateKey = SigningKey.generate(curve=NIST521p)
        self.publicKey = self.privateKey.get_verifying_key().to_string()
        
        hashstr = hashlib.sha256(bytes(self.__str__(), 'utf-8')).hexdigest()
        
        self.alphaTransaction:TransactionData = {
            "timestamp":            time.time(),
            "senderID":             0,
            "receiverID":           0,
            "amount":               100,
            "publicKey":            self.publicKey,
            "signature":            self.privateKey.sign(hashstr),
            "inputHash":            "AlphaTransaction",
            "transactionOutput":    None
        }
        

    def __str__(self) -> str:
        return f"timestamp:{self.alphaTransaction['timestamp']},senderID:{self.alphaTransaction['senderID']},receiverID:{self.alphaTransaction['receiverID']},amount:{self.alphaTransaction['amount']}"
    
    def getAlphaTransaction(self):
        input = TransActionInput()
        self.alphaTransaction["transactionOutput"] = input.generateOutputs(self.alphaTransaction)
        return self.alphaTransaction