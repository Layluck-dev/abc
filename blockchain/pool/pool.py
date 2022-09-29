from flask import jsonify, make_response, Response

from ..types import TransactionData

class Pool():
    def __init__(self) -> None:
        self.list:list[TransactionData] = []
        
    def appendTransaction(self, transaction:TransactionData) -> Response:
        self.list.append(transaction)
        return make_response(jsonify(self.list), 200)