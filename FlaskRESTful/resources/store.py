from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.store import StoreModel

# A `Resource` is one that we can perform CRUD operations on in a RESTful scheme
class StoreList(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    
    # INDEX route
    def get(self):
        return {'allstores': [store.json() for store in StoreModel.query.all()]}

    # CREATE route
    @jwt_required
    def post(self):
        body = StoreList.parser.parse_args()
        if StoreModel.find_store_by_name(body['name']):
            return "This store already exist", 400

        store = StoreModel(body['name'])
        store.save_to_db()

        return "Added store to our stores list.", 201


class Store(Resource):
    # Initialize a parser for this resource
    # parser = reqparse.RequestParser()
    # Notice that for this parser we don't want `name` since we don't want to allow updating
    # of the field `name` and only `price`
    # parser.add_argument('price', type=float)
    # parser.add_argument('store_id', type=int)

    # SHOW route
    def get(self, store_name):
        store = StoreModel.find_store_by_name(store_name)

        if store:
            return store.json()
        else:
            return "This store does not exist -> unable to show.", 400

    # DESTROY route
    @fresh_jwt_required # Make it so that in addition to being logged in as an admin, we also need the token to be fresh
    def delete(self, store_name):
        claim = get_jwt_claims()
        if not claim['is_admin']:
            return "Admin privileges required.", 401

        store = StoreModel.find_store_by_name(store_name)
        if not store:
            return "This store does not exist -> unable to delete.", 400

        store.delete_from_db()
        
        return "Successfully deleted store", 201
        