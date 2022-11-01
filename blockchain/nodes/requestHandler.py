# mypy: ignore-errors
from typing import Tuple

# mypy: ignore-errors
import requests
import json

from ..chain.chain import Chain

from .register import NodeRegistry

class RequestHandler():
    def __init__(self, nodeRegistery:NodeRegistry) -> None:
        self.registry = nodeRegistery
    
    def makeRequest(self, url:str, method:str = "get", body:str | None = None) -> Tuple[str, int]:
        try:
            response = requests.request(method, url, data=body)
            return (json.loads(response.text), response.status_code)
        except:
            return ("\{'info':'An HTTP request error occurred', 'status':500\}", 500)
        
    def pollNodes(self, endpoint:str, method:str = "get", body:str | None = None) -> bool:
        OKs:int = 0
        
        for node in self.registry:
            result = self.makeRequest(node+"/"+endpoint, method, body)
            
            if result[0] == 200:
                OKs += 1
        
        return (100 / len(self.registry) * OKs) > 60
    
    def validateChain(self, chain:Chain) -> bool:
        endpoint = "consensus"
        return self.pollNodes(endpoint, body=json.dumps(chain.chain))
    
    def assertChain(self, chain:Chain) -> None:
        endpoint = "consensus/assert"
        self.pollNodes(endpoint, "post", body=json.dumps(chain.chain))
    
    