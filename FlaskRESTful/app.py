from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import User
from resources.item import Inventory, Item
from auth import authenticate, identity

app = Flask(__name__)

# Connects `data.db` to SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "*T87&*(g99*H"
api = Api(app)

@app.before_first_request
def initialize_db():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Inventory, '/')
api.add_resource(Item, '/<string:item_name>')
api.add_resource(User, '/users')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)
