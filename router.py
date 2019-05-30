from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api
import sys

from resources.transaction import Transaction
from resources.mine import Mine
from resources.chain import Chain
from resources.nodes import Nodes

from blockchain import Blockchain
from uuid import uuid4

#Instantiate the Node
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


#Instantiate the blockchain
blockchain = Blockchain()

#Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')



# Route
api.add_resource(Mine, '/mine', resource_class_kwargs={'blockchain':blockchain, 'node_identifier': node_identifier})
api.add_resource(Transaction, '/transaction/new', resource_class_kwargs={'blockchain':blockchain})
api.add_resource(Chain, '/chain', resource_class_kwargs={'blockchain':blockchain})
api.add_resource(Nodes, '/nodes', resource_class_kwargs={'blockchain':blockchain})

app = Flask(__name__)
app.config.from_object("config")
app.register_blueprint(api_bp, url_prefix='')

#from Model import db
#db.init_app(app)


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(debug=True, port=sys.argv[1])
