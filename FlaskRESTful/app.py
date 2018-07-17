from flask import Flask
from flask import request # This import lets us access the request of the incoming API calls
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import sqlite3

app = Flask(__name__)
app.secret_key = "*T87&*(g99*H"
api = Api(app)

# AUTH CODE ---------------------------------------------
class User:
    def __init__(self, _id, username, pw):
        self.id = _id
        self.username = username
        self.password = pw

    def find_user_by_name(username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
    
        results = cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = results.fetchone()
        connection.close()
    
        if result:
            return User(*result)
        else:
            return None
    
    def find_user_by_id(_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
    
        results = cursor.execute("SELECT * FROM users WHERE id=?", (_id,))
        result = results.fetchone()
        connection.close()
    
        if result:
            return User(*result)
        else:
            return None


def authenticate(un, pw):
    user = User.find_user_by_name(un)
    if user and user.password == pw:
        return user

def identity(payload):
    userid = payload['identity']
    user = User.find_user_by_id(userid)
    return user

jwt = JWT(app, authenticate, identity)
# -------------------------------------------------------

def initialize_db():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    create_item_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
    create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

    cursor.execute(create_item_table)
    cursor.execute(create_user_table)

    connection.close()


class UserResource(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM users")
        users = []
        for result in results:
            users.append({'username': result[1]})

        return {'allusers': users}

    def post(self):
        body = UserResource.parser.parse_args()

        if User.find_user_by_name(body['username']):
            return "This username already exists", 400
        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (body['username'], body['password']))
            
            connection.commit()
            connection.close()
            return "Successfully registered user.", 201


# A `Resource` is one that we can perform CRUD operations on in a RESTful scheme
class Inventory(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('price', type=float, required=True)
    
    # INDEX route
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM items")
        items = []
        for result in results:
            items.append({'name': result[0], 'price': result[1]})

        return {'allitems': items}

    # CREATE route
    @jwt_required()
    def post(self):
        body = Inventory.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM items WHERE name=?", (body['name'],))
        result = results.fetchone()

        if result:
            return "This item already exist", 400
        
        cursor.execute("INSERT INTO items VALUES (?, ?)", (body['name'], body['price']))
        connection.commit()
        connection.close()

        return "Added item to our inventory.", 201


class Item(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    # Notice that for this parser we don't want `name` since we don't want to allow updating
    # of the field `name` and only `price`
    parser.add_argument('price', type=float)

    # SHOW route
    def get(self, item_name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM items WHERE name=?", (item_name,))
        result = results.fetchone()
        connection.close()

        if result:
            return {'name': result[0], 'price': result[1]}
        else:
            return "This item does not exist -> unable to show.", 400

    # UPDATE route
    @jwt_required()
    def put(self, item_name):
        body = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM items WHERE name=?", (item_name,))
        result = results.fetchone()

        if not result:
            return "This item does not exist -> unable to update.", 400
        
        cursor.execute("UPDATE items SET price=? WHERE name=?", (body['price'], item_name))
        connection.commit()
        connection.close()

        return "Successfully updated item", 201

    # DESTROY route
    @jwt_required()
    def delete(self, item_name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM items WHERE name=?", (item_name,))
        result = results.fetchone()

        if not result:
            return "This item does not exist -> unable to delete.", 400
        
        cursor.execute("DELETE FROM items WHERE name=?", (item_name,))
        connection.commit()
        connection.close()

        return "Successfully deleted item", 201


api.add_resource(Inventory, '/')
api.add_resource(Item, '/<string:item_name>')
api.add_resource(UserResource, '/users')


if __name__ == '__main__':
    initialize_db()
    app.run(port=5000, debug=True)
