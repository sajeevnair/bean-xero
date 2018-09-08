from flask_restful import Resource, reqparse
from xero.auth import PublicCredentials
from xero import Xero
from xero.exceptions import XeroException
from models import Contact, Account, SessionHistory, XeroIntegration
from sqlalchemy.exc import SQLAlchemyError


class Verified(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('oauth_token',
                        type=str,
                        required=True,
                        help='oauth_token missing')

    def get(self):
        data = Verified.parser.parse_args()
        session_data = SessionHistory.get_latest(data['oauth_token'])
        credentials = PublicCredentials(**session_data.json())

        try:
            xero = Xero(credentials)
        except XeroException as e:
            return {'message': '{}: {}'.format(e.__class__, e.response)}, 500

        # using consumer key as a placeholder since there is no logged in user
        # here this can be the customer's record for which the data is being pulled
        xero_integration = XeroIntegration.get_by_ckey(
            credentials.state['consumer_key'])

        contacts = xero.contacts.filter(since=xero_integration.updated_on_utc)
        accounts = xero.accounts.filter(since=xero_integration.updated_on_utc)

        updated = False
        message = ''
        try:
            if contacts:
                Contact.sync_with_xero(contacts, xero_integration)
                updated = True
                message += 'Contacts Synced'
            if accounts:
                Account.sync_with_xero(accounts, xero_integration)
                updated = True
                message += ' Accounts Synced'
        except SQLAlchemyError as e:
            return {'message': e._message}, 500
        finally:
            if updated:
                xero_integration.update_date()
            else:
                message = 'Nothing was synced'

        return {'message': message}, 200
