import hashlib
import json
from time import time
import requests

from uuid import uuid4
from urllib.parse import urlparse


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions= []
        
        self.new_block(previous_hash=1, proof=100)
        self.nodes = set() 

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block and adds it to the chain
        """

        block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.current_transactions,
                'proof': proof,
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Reset the current list of transactions
        self.current_transactions = []
        
        self.chain.append(block)
        return block



    def new_transaction(self, sender, recipient, amount):
        """
            Creates a new transaction, adds it to the chain 
            and return the name of the block to which it's added
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amout': amount,
        })
    
        return self.last_block['index'] + 1


    def register_node(self, address):
        """
        Add a new node to the list of nodes
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        #Returns the last Block in the chain
        return self.chain[-1]


    def proof_of_work(self, last_proof): 
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    
    def valid_chain(self, chain):
        """
        Determine the validity of a given blockchain
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self):
        """
        Consensus algorithm: replace our chain by the longest chain on the network
        """
        neighours = self.nodes
        new_chain = None

        #Looking for chain longer
        max_length = len(self.chain)

        for node in neighours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check length and validity
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
