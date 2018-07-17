from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

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
        