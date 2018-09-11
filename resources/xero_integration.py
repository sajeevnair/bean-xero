from flask_restful import Resource, reqparse
from models import XeroIntegration as X


class XeroIntegration(Resource):

    def get(self, xi_id):
        xi = X.get_by_id(xi_id)
        return {'XeroIntegration account': xi.json()}, 200
