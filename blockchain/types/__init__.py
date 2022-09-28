

from datetime import datetime
from typing import TypedDict

class TransactionData(TypedDict):
    timestamp:  datetime
    sender:     int
    receiver:   int
    amount:     float

class BlockData(TypedDict):
    index:        int
    timestamp:    datetime
    proof:        str
    priorHash:    str
    currentHash:  str
    transaction:  TransactionData
