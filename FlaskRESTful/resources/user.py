from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_optional, get_jwt_identity
from models.user import UserModel

class UserList(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    # INDEX route
    @jwt_optional # We set this up so that if you're logged in you can view the list of users with their passwords
    def get(self):
        user_id = get_jwt_identity()
        items = [user.json() for user in UserModel.query.all()]
        if user_id:
            return {'allusers': items}
        else:
            return {'allusers': [item['username'] for item in items]}

    # CREATE route
    def post(self):
        body = UserList.parser.parse_args()

        if UserModel.find_user_by_name(body['username']):
            return "This username already exists.", 400

        body = UserList.parser.parse_args()
        user = UserModel(body['username'], body['password'])
        user.save_to_db()

        return "Successfully registered user.", 201

class User(Resource):
    # SHOW route
    def get(self, user_id):
        user = UserModel.find_user_by_id(user_id)

        if user:
            return user.json()
        else:
            return "This user does not exist -> unable to show.", 400

    # DESTROY route
    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return "This user does not exist -> unable to delete.", 400

        user.delete_from_db()
        
        return "Successfully deleted user.", 201
