from flask import Flask

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Starting CI with the right setup.'