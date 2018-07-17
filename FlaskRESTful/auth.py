from models.user import UserModel

def authenticate(un, pw):
    user = UserModel.find_user_by_name(un)
    if user and user.password == pw:
        return user

def identity(payload):
    userid = payload['identity']
    user = UserModel.find_user_by_id(userid)
    return user
    