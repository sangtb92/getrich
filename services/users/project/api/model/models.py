import time
import datetime
import os
from json import dumps

import jwt
from project import db, bcrypt
from project.api.common.utils import json_serial


class User(db.Model):
    __tablename__ = 'tbl_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    d_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    coin = db.Column(db.DECIMAL, nullable=False, default=0)
    exp = db.Column(db.INTEGER, nullable=False, default=0)
    level = db.Column(db.INTEGER, nullable=False, default=0)
    phone_number = db.Column(db.String(16), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    account_type = db.Column(db.INTEGER, nullable=False, default=0)
    type_extend = db.Column(db.INTEGER, nullable=False, default=0)
    num_guide = db.Column(db.INTEGER, nullable=False, default=0)

    def __init__(self, user_name, password, d_name, phone_number, is_active, is_admin, account_type):
        self.user_name = user_name
        self.d_name = d_name
        self.password = bcrypt.generate_password_hash(
            password, os.getenv('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.phone_number = phone_number
        self.is_active = is_active
        self.is_admin = is_admin
        self.registered_on = datetime.datetime.now()
        self.account_type = account_type

    def to_json(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'd_name': self.d_name,
            'level': self.level,
            'exp': self.exp,
            'last_login': dumps(self.last_login, default=json_serial),
            'registered_on': dumps(self.registered_on, default=json_serial)
        }

    def encode_auth_token(self, user_id):
        """
        Generate auth token
        :param user_id:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload=payload,
                key=os.environ.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.environ.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
