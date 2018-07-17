from flask import Flask
from flask import request # This import lets us access the request of the incoming API calls
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.secret_key = "*T87&*(g99*H"
api = Api(app)

# Temporary data structure to store our items
inven = []

# AUTH CODE ---------------------------------------------
class User:
    def __init__(self, _id, username, pw):
        self.id = _id
        self.username = username
        self.password = pw

users = [User(1, 'brandon', 'password')]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(un, pw):
    user = username_table.get(un, None)
    if user and user.password == pw:
        return user

def identity(payload):
    userid = payload['identity']
    user = userid_table.get(userid, None)
    return user

jwt = JWT(app, authenticate, identity)
# -------------------------------------------------------


# # A `Resource` is one that we can perform CRUD operations on in a RESTful scheme
class Inventory(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('price', type=float, required=True)
    
    # INDEX route
    def get(self):
        return {'allitems': inven}

    # CREATE route
    @jwt_required()
    def post(self):
        body = Inventory.parser.parse_args()
        item = next(filter(lambda x: x['name'] == body['name'], inven), None)

        if item:
            return "This item already exist", 400
        else:
            inven.append(body)
            return "Added item to our inventory.", 201

class Item(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    # Notice that for this parser we don't want `name` since we don't want to allow updating
    # of the field `name` and only `price`
    parser.add_argument('price', type=float)

    # SHOW route
    def get(self, item_name):
        item = next(filter(lambda x: x['name'] == item_name, inven), None)
        if item:
            return {'name': item['name'], 'price':item['price']}
        else:
            return "This item does not exist -> unable to show.", 400

    # UPDATE route
    @jwt_required()
    def put(self, item_name):
        body = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == item_name, inven), None)
        if item:
            item.update(body)
            return "Successfully updated item", 201
        else:
            return "This item does not exist -> unable to update.", 400

    # DESTROY route
    @jwt_required()
    def delete(self, item_name):
        global inven # Need to do this if we're assigning smth to it

        item = next(filter(lambda x: x['name'] == item_name, inven), None)
        if item:
            inven = list(filter(lambda x: x['name'] != item_name, inven))
            return "Successfully deleted item", 201
        else:
            return "This item does not exist -> unable to delete.", 400


api.add_resource(Inventory, '/')
api.add_resource(Item, '/<string:item_name>')

app.run(port=5000, debug=True)
