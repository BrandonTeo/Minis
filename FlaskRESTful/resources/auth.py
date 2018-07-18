from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
from models.user import UserModel
from blacklist import BLACKLIST

class UserLogin(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    # Essentially a POST login endpoint
    def post(self):
        body = UserLogin.parser.parse_args()
        user = UserModel.find_user_by_name(body['username'])

        if user and (user.password == body['password']):
            # Note that we pass in `user.id` as the identity of the token
            # This means that we'll be able to extract that field given a particular token
            access_tkn = create_access_token(identity=user.id, fresh=True)
            refresh_tkn = create_refresh_token(user.id)

            return {'access_token': access_tkn, 'refresh_token': refresh_tkn}, 200

        else:
            return "Invalid credentials -> Unable to log you in.", 401


class UserLogout(Resource):
    @jwt_required # Can only logout if we're logged in
    def post(self):
        # Big idea is to blacklist the unique id of a user's access token so that he can't use the same
        # token to log back in since it'll be in the blacklist
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        
        return "Successfully logged out.", 200


class TokenRefresh(Resource):
    # Essentially, this means that when we POST to this endpoint along with a `refresh_token`,
    # we will give back a new access token that has `fresh=False`
    @jwt_refresh_token_required
    def post(self): # Notice the similarities with the method above ^
        current_userid = get_jwt_identity()
        new_tkn = create_access_token(identity=current_userid, fresh=False)

        return {'access_token': new_tkn}, 200

