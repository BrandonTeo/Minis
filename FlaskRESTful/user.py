from flask_restful import Resource, reqparse
import sqlite3

class User:
    def __init__(self, _id, username, pw):
        self.id = _id
        self.username = username
        self.password = pw

    def find_user_by_name(username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
    
        results = cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = results.fetchone()
        connection.close()
    
        if result:
            return User(*result)
        else:
            return None
    
    def find_user_by_id(_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
    
        results = cursor.execute("SELECT * FROM users WHERE id=?", (_id,))
        result = results.fetchone()
        connection.close()
    
        if result:
            return User(*result)
        else:
            return None


class UserResource(Resource):
    # Initialize a parser for this resource
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM users")
        users = []
        for result in results:
            users.append({'username': result[1]})

        return {'allusers': users}

    def post(self):
        body = UserResource.parser.parse_args()

        if User.find_user_by_name(body['username']):
            return "This username already exists", 400
        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (body['username'], body['password']))
            
            connection.commit()
            connection.close()
            return "Successfully registered user.", 201
