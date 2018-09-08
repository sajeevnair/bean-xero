from db import db


class SessionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    callback_uri = db.Column(db.Text)
    consumer_key = db.Column(db.Text)
    consumer_secret = db.Column(db.Text)
    oauth_authorization_expires_at = db.Column(db.DateTime)
    oauth_expires_at = db.Column(db.DateTime)
    oauth_token = db.Column(db.Text)
    oauth_token_secret = db.Column(db.Text)
    verified = db.Column(db.Boolean)

    def __init__(self,
                 callback_uri,
                 consumer_key,
                 consumer_secret,
                 oauth_authorization_expires_at,
                 oauth_expires_at,
                 oauth_token,
                 oauth_token_secret,
                 verified
                 ):
        self.callback_uri = callback_uri
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_authorization_expires_at = oauth_authorization_expires_at
        self.oauth_expires_at = oauth_expires_at
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.verified = verified

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_latest(cls,oauth_token):
        return cls.query.filter_by(oauth_token=oauth_token).first()

    def json(self):
        return {
            'callback_uri': self.callback_uri,
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'oauth_authorization_expires_at': self.oauth_authorization_expires_at,
            'oauth_expires_at': self.oauth_expires_at,
            'oauth_token': self.oauth_token,
            'oauth_token_secret': self.oauth_token_secret,
            'verified': self.verified
        }
