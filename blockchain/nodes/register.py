from flask import jsonify, make_response, Response

class NodeRegistry():
    def __init__(self, nodes:list[str]) -> None:
        self.registry:list[str] = nodes
        
    def registerNode(self, address:str) -> Response:
        self.registry.append(address)
        return make_response(jsonify(self.registry), 200)
    
    def getNodes(self) -> Response:
        return make_response(jsonify(self.registry), 200)