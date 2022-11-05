from flask import jsonify, make_response, Response
from typing import Any

class NodeRegistry():
    def __init__(self) -> None:
        self.registry:list[str] = []
        
    def registerNode(self, address:Any) -> Response:
        try:
            nodeAddress = str(address["address"])
            self.registry.append(nodeAddress)
            return make_response(jsonify(self.registry), 200)
        except:
            return make_response(jsonify({"info":"malformed request","status":400}), 400)
    
    def getNodes(self) -> Response:
        return make_response(jsonify(self.registry), 200)