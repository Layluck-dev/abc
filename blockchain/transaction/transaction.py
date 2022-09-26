from datetime import datetime
from flask import jsonify, make_response

from ..pool.pool import Pool

class Transaction():
    def __init__(self, pool:Pool) -> None:
        self.pool = pool
        
    def createTransaction(self, transactionReq):
        try:
            transactionData = {
                "timestamp":    datetime.now(),
                "senderID":     int(transactionReq["senderID"]),
                "receiverID":   int(transactionReq["receiverID"]),
                "amount":       float(transactionReq["amount"])
            }
        except:
            return make_response(jsonify({"info":"malformed request", "status":"400"}), 400)
        
        if not transactionData["amount"] > 0:
            return make_response(jsonify({"info":"no cheeky exploits for you", "status":"400"}), 400)
        
        return self.pool.appendTransaction(transactionData)
    