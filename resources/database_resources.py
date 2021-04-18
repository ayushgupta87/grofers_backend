from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.database_model import DatabaseModel


class GetItems(Resource):
    @jwt_required()
    def get(self):
        categoryExists = DatabaseModel.find_all()

        if categoryExists:
            return {'items': list(
                map(lambda x: x.item_json(),
                    DatabaseModel.find_all()))}, 200
        return {'message': 'Items not found'}, 400
