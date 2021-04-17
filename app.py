import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from werkzeug.serving import WSGIRequestHandler

from resources.database_resources import GetItems
from resources.users_resources import RegisterUser, LoginUser, RefreshAccessToken

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ayushApp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'ayushApp'
api = Api(app)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


# users requests
api.add_resource(RegisterUser, '/ayush/api/register')
api.add_resource(LoginUser, '/ayush/api/login')
api.add_resource(RefreshAccessToken, '/ayush/api/refreshToken')

# get items
api.add_resource(GetItems, '/ayush/api/items/<string:item_category>')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    # Flutter error of Connection closed while receiving data > windows OS
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True, port=5000)
