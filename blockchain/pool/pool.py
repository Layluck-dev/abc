from flask import jsonify, make_response, Response

class Pool():
    def __init__(self) -> None:
        self.list = []
        
    def appendTransaction(self, transaction) -> Response:
        self.list.append(transaction)
        return make_response(jsonify(self.list), 200)