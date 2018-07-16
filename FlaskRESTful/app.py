from flask import Flask
from flask import request # This import lets us access the request of the incoming API calls
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Temporary data structure to store our items
inven = []

# # A `Resource` is one that we can perform CRUD operations on in a RESTful scheme
class Inventory(Resource):
    # INDEX route
    def get(self):
        return {'allitems': inven}

    # CREATE route
    def post(self):
        body = request.get_json()
        item = next(filter(lambda x: x['name'] == body['name'], inven), None)

        if item:
            return "This item already exist", 400
        else:
            inven.append(body)
            return "Added item to our inventory.", 201

class Item(Resource):
    # SHOW route
    def get(self, item_name):
        item = next(filter(lambda x: x['name'] == item_name, inven), None)
        if item:
            return {'name': item['name'], 'price':item['price']}
        else:
            return "This item does not exist -> unable to show.", 400

    # UPDATE route
    def put(self, item_name):
        body = request.get_json()
        item = next(filter(lambda x: x['name'] == item_name, inven), None)
        if item:
            item.update(body)
            return "Successfully updated item", 201
        else:
            return "This item does not exist -> unable to update.", 400

    # DESTROY route
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

app.run(port=5000)
