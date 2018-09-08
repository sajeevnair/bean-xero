from db import db
from datetime import datetime
import os


class XeroIntegration(db.Model):
    __tablename__ = 'xero_integration'

    id = db.Column(db.Integer, primary_key=True)

    org_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    website = db.Column(db.Text)
    consumer_key = db.Column(db.Text)
    updated_on_utc = db.Column(db.DateTime, default=datetime(1970, 1, 1))
    contacts = db.relationship('Contact', backref='xint', lazy=True)
    accounts = db.relationship('Account', backref='xint', lazy=True)

    @classmethod
    def create_default(cls):
        org = cls(org_name='Sajeev Nair Inc',
                  email='sales@sajeevnair.net',
                  website='www.sajeevnair.net',
                  consumer_key=os.environ.get('XERO_CONSUMER_KEY'))
        org.save_to_db()

    @classmethod
    def get_by_ckey(cls, ckey):
        return cls.query.filter_by(consumer_key=ckey).first()

    def update_date(self):
        self.updated_on_utc = datetime.utcnow()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
