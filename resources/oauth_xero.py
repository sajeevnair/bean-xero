from flask_restful import Resource, reqparse
from flask import redirect
from xero.auth import PublicCredentials
from xero.exceptions import XeroException
from models import SessionHistory


class OauthXero(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('oauth_token',
                        type=str,
                        required=True,
                        help='oauth_token missing')
    parser.add_argument('oauth_verifier',
                        type=str,
                        required=True,
                        help='oauth_verifier missing')
    parser.add_argument('org', type=str, required=True, help='org missing')

    def get(self):
        data = OauthXero.parser.parse_args()

        session_data = SessionHistory.get_latest(data['oauth_token'])

        credentials = PublicCredentials(**session_data.json())
        try:
            credentials.verify(data['oauth_verifier'])
            s = SessionHistory(**credentials.state)
            s.save_to_db()
            session_data.delete_from_db()

        except XeroException as e:
            return {'message': '{}: {}'.format(e.__class__, e.message)}, 500

        return redirect('/verified?oauth_token={}'.format(credentials.state['oauth_token']))
