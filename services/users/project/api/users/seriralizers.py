from flask_restplus import fields
from project.api.restplus import api

user_data = api.model('User reps', {
    'id': fields.Integer(required=True, description='User id'),
    'user_name': fields.String(required=True, description='User name'),
    'd_name': fields.String(required=True, description='Display name'),
    'level': fields.Integer(required=True, description='User level'),
    'exp': fields.Integer(required=True, description='User experience'),
    'last_login': fields.DateTime(required=True, description='Date of login latest'),
    'registered_on': fields.DateTime(required=True, description='Date of register'),
})
login_reps = api.model('Login Reps', {
    'code': fields.Integer(required=True, description='Response code'),
    'message': fields.String(required=True, description='Response message'),
    'auth_token': fields.String(required=True, description='Auth token'),
    'data': fields.Nested(user_data)
})
