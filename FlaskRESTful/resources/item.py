from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# A `Resource` is one that we can perform CRUD operations on in a RESTful scheme
class ItemList(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('price', type=float, required=True)
    parser.add_argument('store_id', type=int, required=True)
    
    # INDEX route
    def get(self):
        return {'allitems': [item.json() for item in ItemModel.query.all()]}

    # CREATE route
    @jwt_required()
    def post(self):
        body = ItemList.parser.parse_args()
        if ItemModel.find_item_by_name(body['name']):
            return "This item already exist", 400

        item = ItemModel(body['name'], body['price'], body['store_id'])
        item.save_to_db()

        return "Added item to our inventory.", 201


class Item(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    # Notice that for this parser we don't want `name` since we don't want to allow updating
    # of the field `name` and only `price`
    parser.add_argument('price', type=float)
    parser.add_argument('store_id', type=int)

    # SHOW route
    def get(self, item_name):
        item = ItemModel.find_item_by_name(item_name)

        if item:
            return item.json()
        else:
            return "This item does not exist -> unable to show.", 400

    # UPDATE route
    @jwt_required()
    def put(self, item_name):
        item = ItemModel.find_item_by_name(item_name)
        if not item:
            return "This item does not exist -> unable to update.", 400
        
        body = Item.parser.parse_args()
        item.price = body['price']
        item.store_id = body['store_id']
        item.save_to_db()

        return "Successfully updated item", 201

    # DESTROY route
    @jwt_required()
    def delete(self, item_name):
        item = ItemModel.find_item_by_name(item_name)
        if not item:
            return "This item does not exist -> unable to delete.", 400

        item.delete_from_db()
        
        return "Successfully deleted item", 201
        