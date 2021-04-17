import requests
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jti
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.users_model import UserModel

_customer_parser = reqparse.RequestParser()

_customer_parser.add_argument('name',
                              type=str,
                              required=True,
                              help='Name is required')
_customer_parser.add_argument('username',
                              type=str,
                              required=True,
                              help='Username required')
_customer_parser.add_argument('password',
                              type=str,
                              required=True,
                              help='Password Required')
_customer_parser.add_argument('confirm_password',
                              type=str,
                              required=True,
                              help='Confirm Password Required')


class RegisterUser(Resource):
    def post(self):
        data = _customer_parser.parse_args()

        if len(str(data['name']).strip()) > 16:
            return {'message': 'Customer name length exceeding than 16 characters'}, 400

        if len(str(data['username']).strip()) > 16:
            return {'message': 'Customer username length exceeding than 16 characters'}, 400

        if len(str(data['username']).strip()) < 6:
            return {'message': 'username must have six or more than six characters'}, 400

        if len(str(data['password']).strip()) < 6:
            return {'message': 'Password must have six or more than six characters'}, 400

        if len(str(data['password']).strip()) > 16:
            return {'message': 'Password length exceeding than 16 characters'}, 400

        if UserModel.find_by_username(str(data['username']).lower().strip()):
            return {'message': 'username not available'}, 400

        if data['password'] != data['confirm_password']:
            return {'message': 'Password and confirm password not same'}, 400

        try:
            new_user = UserModel(
                str(data['name']).title().strip(),
                str(data['username']).lower().strip(),
                str(data['password'])
            )
            new_user.save_to_db()
            return {'message': 'You are successfully registered'}, 200
        except Exception as e:
            print(f'Exception in adding new user {e}')
            return {'message': 'Something went wrong'}, 500


class LoginUser(Resource):
    def post(self):
        _userlogin = reqparse.RequestParser()
        _userlogin.add_argument('username', type=str, required=True, help='Username is required')
        _userlogin.add_argument('password', type=str, required=True, help='Password is required')

        data = _userlogin.parse_args()

        userCheck = UserModel.find_by_username(str(data['username']).lower().strip())

        if userCheck:
            access_token = create_access_token(identity=userCheck.username, fresh=True)
            refresh_token = create_refresh_token(userCheck.username)

            return {'access_token': access_token,
                    'refresh_token': refresh_token}, 200
        return {'message': 'Invalid credentials'}, 400


class RefreshAccessToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        check_user = UserModel.find_by_username(get_jwt_identity())
        if not check_user:
            return {'message': 'Unauthorized'}, 401
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=True)
        return {'access_token': access_token}, 200


class GetCuttentUser(Resource):

    @jwt_required()
    def get(self):
        userDetails = UserModel.find_by_username(get_jwt_identity())
        if not userDetails:
            return {'message': 'Unauthorized'}, 400
        currentUser = get_jwt_identity()

        if currentUser:
            return {'message': currentUser}, 200
        return {'message': 'Unauthorized'}, 400