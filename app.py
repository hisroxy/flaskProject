from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLALchemy
from werkzeug.security import generate_password_hash
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)