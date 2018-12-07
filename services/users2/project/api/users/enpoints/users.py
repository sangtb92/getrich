import logging
from flask_restplus import Resource

from project.api.users.bussiness import delete_user

from project.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('users', description='Api liên quan tới người dùng.')


@ns.route('/delete')
class UserDelete(Resource):
    def post(self):
        """
        return result user register
        """
        resp = delete_user()
        return resp, resp.get('code')
