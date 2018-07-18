from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserList, User
from resources.item import ItemList, Item
from resources.store import StoreList, Store
from resources.auth import UserLogin, TokenRefresh, UserLogout
from blacklist import BLACKLIST

app = Flask(__name__)

# Connects `data.db` to SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Allow other modules/packages to raise exceptions/errors
app.config['PROPAGATE_EXCEPTIONS'] = True

# Blacklist configurations
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = "*T87&*(g99*H"
api = Api(app)

@app.before_first_request
def initialize_db():
    db.create_all()

jwt = JWTManager(app)

# ---------------------------------------------------------------------------
# Attach a claim to our access tokens
# With this, whenever an access token is required, there will be a claim attached with it
# Example Usage: Admin authorization 
@jwt.user_claims_loader
def add_claims(identity): # `identity` here is a field inside the access token
    # `1` here is a hard coded example
    return {'is_admin': True} if identity == 1 else {'is_admin': False}
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Example Usage: Logout functionality
@jwt.token_in_blacklist_loader
def in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback():
    return "This token has been revoked.", 401
# ---------------------------------------------------------------------------


api.add_resource(ItemList, '/')
api.add_resource(Item, '/<string:item_name>')

api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/stores/<string:store_name>')

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>')

api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)
