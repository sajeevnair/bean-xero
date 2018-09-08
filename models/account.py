from db import db


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)

    xero_account_id = db.Column(db.String(100), nullable=False, unique=True)
    account_name = db.Column(db.String(100))
    code = db.Column(db.String(20))
    account_type = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    enable_payment_to_account = db.Column(db.Boolean)
    account_class = db.Column(db.String(15))
    description = db.Column(db.Text)
    system_account = db.Column(db.String(20))
    bank_account_number = db.Column(db.String(50))
    bank_account_type = db.Column(db.String(20))
    currency_code = db.Column(db.String(5))

    tax_type = db.Column(db.String(20))
    show_in_expense_claim = db.Column(db.Boolean)

    reporting_code = db.Column(db.String(20))
    reporting_code_name = db.Column(db.String(20))
    has_attachments = db.Column(db.Boolean)
    updated_date_utc = db.Column(db.DateTime)
    xint_id = db.Column(db.Integer, db.ForeignKey(
        'xero_integration.id'), nullable=False)
        

    def json(self):
        return {
            'xero_account_id': self.xero_account_id,
            'name': self.account_name,
            'code': self.code,
            'account_type': self.account_type,
            'enable_payment_to_account': self.enable_payment_to_account,
            'status': self.status,
            'account_class': self.account_class,
            'description': self.description,
            'system_account': self.system_account,
            'bank_account_number': self.bank_account_number,
            'bank_account_type': self.bank_account_type,
            'currency_code': self.currency_code,
            'tax_type': self.tax_type,
            'show_in_expense_claim': self.show_in_expense_claim,
            'reporting_code': self.reporting_code,
            'reporting_code_name': self.reporting_code_name,
            'has_attachments': self.has_attachments
        }

    @classmethod
    def make_form_xero(cls, xero_account, xint):
        return cls(
            xero_account_id=xero_account.get('AccountID'),
            account_name=xero_account.get('Name'),
            code=xero_account.get('Code'),
            account_type=xero_account.get('Type'),
            enable_payment_to_account=xero_account.get(
                'EnablePaymentsToAccount'),
            status=xero_account.get('Status'),
            account_class=xero_account.get('Class'),
            description=xero_account.get('Description'),
            system_account=xero_account.get('SystemAccount'),
            bank_account_number=xero_account.get('BankAccountNumber'),
            bank_account_type=xero_account.get('BankAccountType'),
            currency_code=xero_account.get('CurrencyCode'),
            tax_type=xero_account.get('TaxType'),
            show_in_expense_claim=xero_account.get(
                'ShowInExpenseClaims', False),
            reporting_code=xero_account.get('ReportingCode'),
            reporting_code_name=xero_account.get('ReportingCodeName'),
            has_attachments=xero_account.get('HasAttachments', False),
            updated_date_utc=xero_account.get('UpdatedDateUTC'),
            xint=xint
        )

    @classmethod
    def sync_with_xero(cls, xero_accounts, xint):
        if cls.is_table_empty(xint.id):
            cls.add(xero_accounts, xint)
        else:
            cls.replace_outdated(xero_accounts, xint)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def add(cls, xero_accounts, xint):
        for xero_account in xero_accounts:
            account = cls.make_form_xero(xero_account, xint)
            db.session.add(account)
        db.session.commit()

    @classmethod
    def replace_outdated(cls, xero_accounts, xint):
        for xero_account in xero_accounts:
            account = cls.make_form_xero(xero_account, xint)
            old = cls.query.filter_by(
                xero_account_id=account.xero_account_id, xint_id=xint.id).first()
            if old:
                if old.updated_date_utc < account.updated_date_utc:
                    db.session.delete(old)
                    db.session.add(account)
            else:
                db.session.add(account)
        db.session.commit()

    @classmethod
    def find_by_id(cls, c_id):
        return cls.query.filter_by(id=c_id).first()

    @classmethod
    def is_table_empty(cls, xint_id):
        return cls.query.filter_by(xint_id=xint_id).first() is None
