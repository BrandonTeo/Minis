from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    # INDEX route
    def get(self):
        return {'allusers': [user.json() for user in UserModel.query.all()]}

    # CREATE route
    def post(self):
        body = User.parser.parse_args()

        if UserModel.find_user_by_name(body['username']):
            return "This username already exists", 400

        body = User.parser.parse_args()
        user = UserModel(body['username'], body['password'])
        user.save_to_db()

        return "Successfully registered user.", 201

