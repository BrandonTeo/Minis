from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import sqlite3

from user import User, UserResource
from item import Inventory, Item

app = Flask(__name__)
app.secret_key = "*T87&*(g99*H"
api = Api(app)

# AUTH CODE ---------------------------------------------
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

api.add_resource(Inventory, '/')
api.add_resource(Item, '/<string:item_name>')
api.add_resource(UserResource, '/users')

def initialize_db():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    create_item_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
    create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

    cursor.execute(create_item_table)
    cursor.execute(create_user_table)

    connection.close()

if __name__ == '__main__':
    initialize_db()
    app.run(port=5000, debug=True)
