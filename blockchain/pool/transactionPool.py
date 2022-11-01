from typing import Any, Tuple
from flask import jsonify, make_response, Response

from ..types import TransActionOutput, TransactionOutputs

class TransactionPool():
    def __init__(self) -> None:
        self.list:list[TransActionOutput] = []
        
    def appendTransaction(self, transactionOutput:TransActionOutput) -> None:
        self.list.append(transactionOutput)
        
    def appendTransactions(self, outputs:TransactionOutputs) -> None:
        self.list.append(outputs[0])
        self.list.append(outputs[1])
        
    def pollPool(self) -> Response:
        return make_response(jsonify(self.list), 200)
    
    def find(self, idOrHash:str) -> Tuple[int, TransActionOutput|None]:        
        for i, transactionOutput in enumerate(self.list):
            if transactionOutput["id"] == idOrHash:
                return (i, transactionOutput)
            
            if transactionOutput["hash"] == idOrHash:
                return (i, transactionOutput)
            
        return (-1, None)

    def get(self, idOrHash:str, remove:bool=False) -> TransActionOutput | None:
        result = self.find(idOrHash)
        
        if result[0] == -1:
            return None
        
        if remove:
            self.list.pop(result[0])
            
        return result[1]
    
    def remove(self, idOrHash) -> Response:
        result = self.get(idOrHash, True)
        
        if not result:
            return make_response(jsonify({"info": "transactionoutput not found", "status": "404"}), 404)
        
        return make_response(jsonify(result), 200)
    
    def pollOutput(self, transactionReq:Any) -> Response:
        try:
            requestData = {
                "id":   str(transactionReq["id"]),
                "hash": str(transactionReq["hash"]),
            }
        except:
            return make_response(jsonify({"info":"malformed request", "status":"400"}), 400)
        
        result = self.get(requestData["hash"]+requestData["id"])
        
        if not result:
            return make_response(jsonify({"info": "transactionOutput not found"}), 404)
        
        return make_response(jsonify(result), 200)
    
    def openRemainderByUid(self, userID:int) -> TransActionOutput | None:
        for transaction in self.list:
            if transaction["receiverID"] == userID and transaction["isRemainder"]:
                return transaction
        
        return None
    
    def getOpenRemainder(self, userID:int) -> Response:
        result = self.openRemainderByUid(userID)
        
        if not result:
            return make_response(jsonify({"info": "no open transaction found for this user", "status": "404"}), 404)
        
        return make_response(jsonify(result))