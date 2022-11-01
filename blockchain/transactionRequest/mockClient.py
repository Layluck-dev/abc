
import hashlib
import time
from ..types import TransactionData

# mypy: ignore-errors
from ecdsa import SigningKey, NIST521p

class Client:
    def __init__(self) -> None:
        self.privateKey = SigningKey.generate(curve=NIST521p)
        self.publicKey = self.privateKey.get_verifying_key().to_string()
        
        hashstr = hashlib.sha256(bytes(self.__str__(), 'utf-8')).hexdigest()
        
        self.pseudoTransaction:TransactionData = {
            "timestamp":            time.time(),
            "senderID":             3,
            "receiverID":           12,
            "amount":               77.4,
            "publicKey":            self.publicKey,
            "signature":            self.privateKey.sign(hashstr),
            "inputHash":            "AlphaTransaction",
            "transactionOutput":    None
        }

    def __str__(self) -> str:
        return f"timestamp:{self.pseudoTransaction['timestamp']},senderID:{self.pseudoTransaction['senderID']},receiverID:{self.pseudoTransaction['receiverID']},amount:{self.pseudoTransaction['amount']}"