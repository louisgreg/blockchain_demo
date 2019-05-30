from flask import jsonify, request
from flask_restful import Resource
from blockchain import Blockchain


class Transaction(Resource):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def post(self):
        values = request.get_json()

        #Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        #Create a new Transaction
        index = self.blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        
        response = {'message': f'Transaction will be added to Block {index}'}
        return response, 201
