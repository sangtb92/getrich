import datetime, time

from project.api.model.models import User
from project import db, bcrypt
from project.api.common.constant import BAD_REQUEST


def create_user(data):
    user_name = data.get('user_name')
    d_name = data.get('d_name')
    password = data.get('password')
    phone = data.get('phone')
    try:
        user = User.query.filter_by(user_name=user_name).first()
        if not user:
            db.session.add(
                User(user_name=user_name, password=password, d_name=d_name, phone_number=phone, is_active=True,
                     is_admin=True, account_type=0))
            db.session.commit()
            response_object = {
                'code': 201,
                'message': 'create succeeded.'
            }
            return response_object
        else:
            response_object = {
                'code': 400,
                'message': 'user already existed.'
            }
            return response_object
    except Exception as e:
        print(e.__str__())
        response_object = {
            'code': 500,
            'message': e.__str__()
        }
        return response_object


def login(data):
    user_name = data.get('user_name')
    password = data.get('password')
    try:
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                auth_token = user.encode_auth_token(user_id=user.id)
                print(auth_token)
                if auth_token:
                    response_object = {
                        'code': 200,
                        'message': 'login success',
                        # covert bytes to string
                        'auth_token': auth_token.decode("utf-8"),
                        'data': user.to_json()
                    }
                    user.last_login = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                    db.session.commit()
                    return response_object
        else:
            response_object = {
                'code': 400,
                'message': 'Login fail'
            }
            return response_object
    except Exception as e:
        print(e.__str__())
        response_object = {
            'code': 500,
            'message': e.__str__()
        }
        return response_object
