from flask_restful import Resource
from blockchain import Blockchain


class Chain(Resource):
    def __init__(self, **kwargs):
        print("Bonjour         ", kwargs)
        self.blockchain = kwargs['blockchain']

    def get(self):
        response = {
            'chain': self.blockchain.chain,
            'length': len(self.blockchain.chain),
        }
        return response, 200
