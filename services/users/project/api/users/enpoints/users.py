import logging
from flask import request
from flask_restplus import Resource

from project.api.users.bussiness import create_user, login
from project.api.users.seriralizers import login_reps
from project.api.users.parser import user_arguments, user_login_arguments

from project.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('users', description='Api liên quan tới người dùng.')


@ns.route('/ping')
class UserPing(Resource):
    @api.response(200, 'pong')
    def get(self):
        """
        return pong
        """
        return 'pong', 200


@ns.route('/register')
class UserRegister(Resource):
    @api.expect(user_arguments)
    @api.response('201', 'Create user succeeded')
    def post(self):
        """
        return result user register
        """
        resp = create_user(user_arguments.parse_args(request))
        return resp, resp.get('code')


@ns.route('/login')
class UserLogin(Resource):
    @api.expect(user_login_arguments)
    @api.marshal_with(login_reps)
    def post(self):
        """
        return result user register
        """
        resp = login(user_login_arguments.parse_args(request))
        return resp, resp.get('code')


@ns.route('/<int:user_id>')
class GetUser(Resource):
    @api.expect(user_arguments)
    @api.response('201', 'Create user succeeded')
    def get(self):
        """
        return result user register
        """
        resp = create_user(user_arguments.parse_args(request))
        return resp, resp.get('code')
