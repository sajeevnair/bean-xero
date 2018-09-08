from flask_restful import Resource, reqparse
from flask import redirect
from xero.auth import PublicCredentials
import os
from models import SessionHistory
from sqlalchemy.exc import SQLAlchemyError


class AuthXero(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        consumer_key = os.environ.get('XERO_CONSUMER_KEY')
        consumer_secret = os.environ.get('XERO_CONSUMER_SECRET')

        if consumer_key is None or consumer_secret is None:
            return {
                'message': 'XERO_CONSUMER_KEY \
                 and XERO_CONSUMER_SECRET are required'}, 400

        credentials = PublicCredentials(
            consumer_key,
            consumer_secret,
            callback_uri='https://bean-xero.herokuapp.com/oauth')

        s = SessionHistory(**credentials.state)
        try:
            s.save_to_db()
        except SQLAlchemyError as e:
            return {'message': e._message}, 500

        return redirect(credentials.url)
