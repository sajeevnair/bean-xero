from db import db


class Contact(db.Model):
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)

    xero_contact_id = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(100))
    account_number = db.Column(db.String(100))
    contact_status = db.Column(db.String(10))
    contact_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.Text)
    skype_username = db.Column(db.Text)
    bank_account_number = db.Column(db.String(50))
    tax_number = db.Column(db.String(30))
    accounts_receivable_tax_type = db.Column(db.String(10))
    account_payable_tax_type = db.Column(db.String(30))
    default_currency = db.Column(db.String(10))
    updated_date_utc = db.Column(db.DateTime)
    xero_network_key = db.Column(db.String(100))
    sales_default_account_code = db.Column(db.String(20))
    purchases_default_account_code = db.Column(db.String(20))
    sales_tracking_categories = db.Column(db.PickleType)
    purchase_tracking_categories = db.Column(db.PickleType)
    tracking_category_name = db.Column(db.String(20))
    tracking_options_name = db.Column(db.String(20))
    payment_terms = db.Column(db.String(20))
    contact_groups = db.Column(db.PickleType)
    website = db.Column(db.Text)
    branding_theme = db.Column(db.Text)
    discount = db.Column(db.Float)
    balances = db.Column(db.PickleType)
    has_attachments = db.Column(db.Boolean)
    is_supplier = db.Column(db.Boolean)
    is_customer = db.Column(db.Boolean)
    addresses = db.Column(db.PickleType)
    phones = db.Column(db.PickleType)
    contact_persons = db.Column(db.PickleType)
    xint_id = db.Column(db.Integer, db.ForeignKey(
        'xero_integration.id'), nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def is_table_empty(cls, xint_id):
        return cls.query.filter_by(xint_id=xint_id).first() is None

    @classmethod
    def make_form_xero(cls, xero_contact, xint):
        return cls(
            xero_contact_id=xero_contact.get('ContactID'),
            contact_number=xero_contact.get('ContactNumber'),
            account_number=xero_contact.get('AccountNumber'),
            contact_status=xero_contact.get('ContactStatus'),
            contact_name=xero_contact.get('Name'),
            first_name=xero_contact.get('FirstName'),
            last_name=xero_contact.get('LastName'),
            email=xero_contact.get('EmailAddress'),
            skype_username=xero_contact.get('SkypeUserName'),
            bank_account_number=xero_contact.get('BankAccountDetails'),
            tax_number=xero_contact.get('TaxNumber'),
            accounts_receivable_tax_type=xero_contact.get(
                'AccountsReceivableTaxType'),
            account_payable_tax_type=xero_contact.get(
                'AccountsPayableTaxType'),
            addresses=xero_contact.get('Addresses'),
            phones=xero_contact.get('Phones'),
            default_currency=xero_contact.get('DefaultCurrency'),
            updated_date_utc=xero_contact.get('UpdatedDateUTC'),
            contact_persons=xero_contact.get('ContactPersons'),
            xero_network_key=xero_contact.get('XeroNetworkKey'),
            sales_default_account_code=xero_contact.get(
                'SalesDefaultAccountCode'),
            purchases_default_account_code=xero_contact.get(
                'PurchasesDefaultAccountCode'),
            sales_tracking_categories=xero_contact.get(
                'SalesTrackingCategories'),
            purchase_tracking_categories=xero_contact.get(
                'PurchasesTrackingCategories'),
            tracking_category_name=xero_contact.get('TrackingCategoryName'),
            tracking_options_name=xero_contact.get('TrackingOptionName'),
            payment_terms=xero_contact.get('PaymentTerms'),
            contact_groups=xero_contact.get('ContactGroups'),
            website=xero_contact.get('Website'),
            branding_theme=xero_contact.get('BrandingTheme'),
            discount=xero_contact.get('Discount'),
            balances=xero_contact.get('Balances'),
            has_attachments=xero_contact.get('HasAttachments'),
            is_supplier=xero_contact.get('isSupplier', False),
            is_customer=xero_contact.get('isCustomer', False),
            xint=xint
        )

    @classmethod
    def add(cls, xero_contacts, xint):

        for xero_contact in xero_contacts:
            contact = cls.make_form_xero(xero_contact, xint)
            db.session.add(contact)
        db.session.commit()

    @classmethod
    def replace_outdated(cls, xero_contacts, xint):
        for xero_contact in xero_contacts:
            contact = cls.make_form_xero(xero_contact, xint)
            old = cls.query.filter_by(
                xero_contact_id=contact.xero_contact_id, xint_id=xint.id).first()
            if old:
                if old.updated_date_utc < contact.updated_date_utc:
                    db.session.delete(old)
                    db.session.add(contact)
            else:
                db.session.add(contact)
        db.session.commit()

    @classmethod
    def sync_with_xero(cls, xero_contacts, xint):
        if cls.is_table_empty(xint.id):
            cls.add(xero_contacts, xint)
        else:
            cls.replace_outdated(xero_contacts, xint)

    @classmethod
    def find_by_id(cls, c_id):
        return cls.query.filter_by(id=c_id).first()

    def json(self):
        return {
            'id': self.id,
            'xero_contact_id': self.xero_contact_id,
            'account_number': self.account_number,
            'status': self.contact_status,
            'name': self.contact_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'addresses': self.addresses,
            'phones': self.phones,
            'contact_groups': self.contact_groups,
            'balances': self.balances
        }

# Out of scope for now


# class Phone(db.Model):
#     __tablename__ = 'phone'

#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.String(50))
#     area_code = db.Column(db.String(10))
#     country_code = db.Column(db.String(20))
#     phone_type = db.Column(db.String(10))
#     contact_id = db.Column(db.Integer, db.ForeignKey(
#         'contact.id'), nullable=False)


# class Address(db.Model):
#     __tablename__ = 'address'
#     id = db.Column(db.Integer, primary_key=True)
#     address_type = db.Column(db.String(10))
#     address_line1 = db.Column(db.String(500))
#     address_line2 = db.Column(db.String(500))
#     address_line3 = db.Column(db.String(500))
#     address_line4 = db.Column(db.String(500))
#     city = db.Column(db.String(255))
#     region = db.Column(db.String(255))
#     country = db.Column(db.String(50))
#     postal_code = db.Column(db.String(50))
#     attention_to = db.Column(db.String(255))

#     contact_id = db.Column(db.Integer, db.ForeignKey(
#         'contact.id'), nullable=False)

#     def __init__(self,
#                  address_type,
#                  address_line1,
#                  address_line2,
#                  address_line3,
#                  address_line4,
#                  city,
#                  region,
#                  country,
#                  postal_code,
#                  attention_to,
#                  ):
#         self.address_type = address_type
#         self.address_line1 = address_line1
#         self.address_line2 = address_line2
#         self.address_line3 = address_line3
#         self.address_line4 = address_line4
#         self.city = city
#         self.region = region
#         self.country = country
#         self.postal_code = postal_code
#         self.attention_to = attention_to

#     def json(self):
#         return {
#             'address_type': self.address_type,
#             'address_line1': self.address_line1,
#             'address_line2': self.address_line2,
#             'address_line3': self.address_line3,
#             'address_line4': self.address_line4,
#             'city': self.city,
#             'region': self.region,
#             'country': self.country,
#             'postal_code': self.postal_code,
#             'attention_to': self.attention_to

#         }


# class ContactPerson(db.Model):
#     __tablename__ = 'contact_person'

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50))
#     last_name = db.Column(db.String(50))
#     email = db.Column(db.Text)
#     include_in_emails = db.Column(db.Boolean)
#     contact_id = db.Column(db.Integer, db.ForeignKey(
#         'contact.id'), nullable=False)

#     def __init__(self,
#                  first_name,
#                  last_name,
#                  email,
#                  include_in_emails):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.include_in_emails = include_in_emails
