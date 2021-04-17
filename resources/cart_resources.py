from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from models.cart_model import CartModel
from models.database_model import DatabaseModel
from models.users_model import UserModel

_add_cart_parser = reqparse.RequestParser()
_add_cart_parser.add_argument('item',
                              type=str,
                              required=True,
                              help='Username required')
_add_cart_parser.add_argument('kg',
                              type=str,
                              required=False,
                              default='5')
_add_cart_parser.add_argument('qty',
                              type=str,
                              required=False,
                              default='1')


class AddItemToCart(Resource):
    @jwt_required()
    def post(self):

        userDetails = UserModel.find_by_username(get_jwt_identity())
        if not userDetails:
            return {'message': 'Unauthorized'}, 400
        currentUser = get_jwt_identity()

        data = _add_cart_parser.parse_args()

        inDbCheck = DatabaseModel.find_all_by_name(str(data['item']).title().strip())
        if not inDbCheck:
            return {'message': 'Requested item not in database'}, 400

        if str(data['qty']).isnumeric():
            print('true, Is numeric')
        else:
            return {'message': 'Quantity must be in numerical'}, 400

        checkItem = CartModel.find_by_username_item_cart(str(currentUser).lower().strip(),
                                                         str(data['item']).title().strip())

        if checkItem:
            return {'message': 'Item already in your database'}, 400
        try:
            addItemToCart = CartModel(
                str(currentUser).lower().strip(),
                str(data['item']).title().strip(),
                data['qty'],
                data['kg'],
                inDbCheck.price_per_kg,
            )
            addItemToCart.save_to_db()
            return {'message': 'Item added to your cart'}, 200
        except Exception as e:
            print(f'Exception while adding to cart {e}')
            return {'message': 'Something went wrong'}, 500


class DeleteItemFromCart(Resource):
    @jwt_required()
    def delete(self, item):
        userDetails = UserModel.find_by_username(get_jwt_identity())
        if not userDetails:
            return {'message': 'Unauthorized'}, 400
        currentUser = get_jwt_identity()

        checkItem = CartModel.find_by_username_item_cart(str(currentUser).lower().strip(),
                                                         str(item).title().strip())

        if not checkItem:
            return {'message': 'Requested item not in your cart'}, 400
        checkItem.delete_from_db()
        return {'message': f'{item} deleted successfully from your cart'}, 200


class EditQty(Resource):
    @jwt_required()
    def put(self, item, qty):
        userDetails = UserModel.find_by_username(get_jwt_identity())
        if not userDetails:
            return {'message': 'Unauthorized'}, 400
        currentUser = get_jwt_identity()

        checkItem = CartModel.find_by_username_item_cart(str(currentUser).lower().strip(),
                                                         str(item).title().strip())

        if not checkItem:
            return {'message': 'Requested item not in your cart'}, 400

        if qty.isnumeric():
            print('true, Is numeric')
        else:
            return {'message': 'Quantity must be in numerical'}, 400
        try:
            checkItem.qty = str(qty)
            return {'message': 'Quantity updated'}, 200
        except Exception as e:
            print(f'Exception while updating quantity {e}')
            return {'message': 'Something went wrong'}, 500



