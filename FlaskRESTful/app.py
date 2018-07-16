from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "You have reached the home route!!!"

app.run(port=5000)
