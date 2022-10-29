import time
from typing import Any
from flask import jsonify, make_response
from ..chain.chain import Chain

from ..pool.transactionPool import TransactionPool
from ..transaction.verification import TransactionVerification
from ..transactionRequest.mockClient import Client

from ..transaction.input import TransActionInput
from ..types import TransactionData
from ..pool.pool import Pool

class Transaction():
    def __init__(self, pool:Pool, transactionOutputs:TransactionPool, chain:Chain) -> None:
        self.pool = pool
        self.transactionOutputs = transactionOutputs
        self.chain = chain
        
    def createTransaction(self, transactionReq:Any):
        try:
            transactionData:TransactionData = {
                "timestamp":            time.time(),
                "senderID":             int(transactionReq["senderID"]),
                "receiverID":           int(transactionReq["receiverID"]),
                "amount":               float(transactionReq["amount"]),
                "publicKey":            str(transactionReq["publicKey"]),
                "signature":            str(transactionReq["signature"]),
                "inputHash":            str(transactionData["inputHash"]),
                "transactionOutput":    None
            }
        except:
            return make_response(jsonify({"info":"malformed request", "status":"400"}), 400)
        
        if not transactionData["amount"] >= 0:
            return make_response(jsonify({"info":"no cheeky exploits for you", "status":"400"}), 400)
        
        #Temporarily mock a transaction, because there is no client currently
        mockClient = Client()
        transactionData = mockClient.pseudoTransaction
        
        balance = self.chain.getBalanceByUid(transactionData["senderID"])
                
        transactionVerification = TransactionVerification(transactionData, balance)
        if not transactionVerification.verifyTransaction():
            return make_response(jsonify({"info":"signature does not resolve", "status":"401"}), 401)
        
        inputObject = TransActionInput()
        outputs = inputObject.generateOutputs(transactionData)
        self.transactionOutputs.appendTransactions(outputs)
        transactionData["transactionOutput"] = outputs
    
        return self.pool.appendTransaction(transactionData)
    