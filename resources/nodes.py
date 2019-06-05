from flask import request
from flask_restful import Resource
from blockchain import Blockchain

class Nodes(Resource):
    def __init__(self, **kwargs):
        self.blockchain = kwargs['blockchain']

    def get(self):
        """
        Apply the consensus
        """
        replaced = self.blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': self.blockchain.chain
            }
        
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': self.blockchain.chain
            }
        return response, 200


    

    def post(self):
        """
        Register a new node
        """
        values = request.get_json()
        nodes = values.get('nodes')
        if nodes is None:
            return "Error: Please supply a valid list of nodes", 400
        
        for node in nodes:
            self.blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(self.blockchain.nodes),
        }
        return response, 200

