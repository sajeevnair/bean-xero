import os
from flask import Flask, render_template, redirect, jsonify, request
from urllib.parse import parse_qsl, urlparse

from resources import OauthXero, AuthXero, Verified
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'redis'
app.secret_key = os.urandom(24)

api = Api(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(AuthXero, '/auth')
api.add_resource(OauthXero, '/oauth')
api.add_resource(Verified, '/verified')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
