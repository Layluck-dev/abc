from typing import Tuple
from flask import jsonify, make_response, Response

from ..types import TransActionOutput

class TransactionPool():
    def __init__(self) -> None:
        self.list:list[TransActionOutput] = []
        
    def appendTransaction(self, transactionOutput:TransActionOutput) -> None:
        self.list.append(transactionOutput)
        
    def pollPool(self) -> Response:
        return make_response(jsonify(self.list), 200)
    
    def get(self, idOrHash:str, remove:bool=False) -> Response:
        result = self.find(idOrHash)
        
        if result[0] == -1:
            return make_response(jsonify({"info": "transactionoutput not found", "status": "404"}), 404)
        
        if remove:
            self.list.pop(result[0])
            
        return make_response(jsonify(result[1]), 200)
    
    def find(self, idOrHash:str) -> Tuple[int, TransActionOutput|None]:        
        for i, transactionOutput in enumerate(self.list):
            if transactionOutput["id"] == idOrHash:
                return (i, transactionOutput)
            
            if transactionOutput["hash"] == idOrHash:
                return (i, transactionOutput)
            
        return (-1, None)
