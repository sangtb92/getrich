from flask_restplus import reqparse

user_arguments = reqparse.RequestParser()
user_arguments.add_argument('user_name', type=str, required=True, help='User name')
user_arguments.add_argument('d_name', type=str, required=True, help='Display name')
user_arguments.add_argument('password', type=str, required=True, help='User\'s password')
user_arguments.add_argument('phone', type=str, required=True, help='User\'s phone')

user_login_arguments = reqparse.RequestParser()
user_login_arguments.add_argument('user_name', type=str, required=True, help='User name')
user_login_arguments.add_argument('password', type=str, required=True, help='Password')
