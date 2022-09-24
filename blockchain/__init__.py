from flask import Flask, jsonify, make_response, request

def launchServer(test_config=None):
    server = Flask(__name__)
    chain = None
    pool = None
    transaction = None
    baseUrl = "/api"
    
    @server.post(baseUrl + 'transaction/new')
    def createTransaction():
        return None

    @server.get(baseUrl + 'pool/index')
    def getPool():
        return None
