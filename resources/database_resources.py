from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.database_model import DatabaseModel


class GetItems(Resource):
    @jwt_required()
    def get(self, item_category):
        categoryExists = DatabaseModel.find_all_by_category(str(item_category).lower().strip())

        if categoryExists:
            return {'items': list(
                map(lambda x: x.item_json(),
                    DatabaseModel.find_all_by_category(str(item_category).lower().strip())))}, 200
        return {'message': 'Items not found'}, 400
