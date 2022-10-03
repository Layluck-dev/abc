
from datetime import datetime
from typing import TypedDict

class TransactionData(TypedDict):
    timestamp:  float
    senderID:   int
    receiverID: int
    amount:     float

class BlockData(TypedDict):
    index:        int
    timestamp:    float
    proof:        int
    priorHash:    str
    currentHash:  str
    transaction:  TransactionData
