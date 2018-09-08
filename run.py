from app import app
from db import db
from models import XeroIntegration
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    XeroIntegration.create_default()

