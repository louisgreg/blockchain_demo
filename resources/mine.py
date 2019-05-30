from flask_restful import Resource


class Mine(Resource):
    def __init__(self, **kwargs):
        print("Bonjour         ", kwargs)
        self.blockchain = kwargs['blockchain']
        self.node_identifier =kwargs['node_identifier']

    def get(self):
        # We run the proof of work algo to get the next proof
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        proof = self.blockchain.proof_of_work(last_proof)

        # We must receive a reward for finding the proof
        # The sender is "0" to signify that this node has mined a new coined
        self.blockchain.new_transaction(
            sender="0",
            recipient=self.node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

        return response, 200
