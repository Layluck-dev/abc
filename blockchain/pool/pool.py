from flask import jsonify, make_response, Response

from ..types import BlockData, TransactionData

class Pool():
    def __init__(self) -> None:
        self.list:list[BlockData] = []
        
    def appendTransaction(self, transaction:TransactionData) -> Response:
        self.list.append(transaction)
        return make_response(jsonify(self.list), 200)