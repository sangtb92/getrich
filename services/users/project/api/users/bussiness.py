import datetime

from project.api.model.models import User, BlacklistToken
from project import db, bcrypt


def create_user(data):
    user_name = data.get('user_name')
    d_name = data.get('d_name')
    password = data.get('password')
    phone = data.get('phone')
    try:
        user = User.query.filter_by(user_name=user_name).first()
        if not user:
            new_user = User(user_name=user_name, password=password, d_name=d_name, phone_number=phone, is_active=True,
                            is_admin=False, account_type=0)
            db.session.add(new_user)
            db.session.commit()
            response_object = {
                'code': 201,
                'message': 'success',
                'data': new_user.to_json()
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
                if auth_token:
                    response_object = {
                        'code': 200,
                        'message': 'success',
                        # covert bytes to string
                        'auth_token': auth_token.decode(),
                        'data': user.to_json()
                    }
                    user.last_login = datetime.datetime.now()
                    db.session.commit()
                    return response_object
        else:
            response_object = {
                'code': 400,
                'message': 'User doesn\'t exist.'
            }
            return response_object
    except Exception as e:
        print(e.__str__())
        response_object = {
            'code': 500,
            'message': e.__str__()
        }
        return response_object


def get_list_user(data):
    auth_header = data.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            users = User.query.all()
            user_arr = []
            for u in users:
                user_arr.append(u.to_json())
            response_object = {
                'code': 200,
                'status': 'success',
                'data': user_arr
            }
        else:
            response_object = {
                'code': 400,
                'status': 'fail',
                'message': resp
            }
    else:
        response_object = {
            'code': 400,
            'message': 'User doesn\'t exist.',
            'auth_token': auth_token
        }
    return response_object


def get_user(data):
    auth_header = data.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user_id = data.headers.get('user_id')
            user = User.query.filter_by(id=user_id).first()
            response_object = {
                'code': 200,
                'status': 'success',
                'data': user.to_json()
            }
        else:
            response_object = {
                'code': 400,
                'status': 'fail',
                'message': resp
            }
    else:
        response_object = {
            'code': 400,
            'message': 'User doesn\'t exist.'
        }
    return response_object


def logout(data):
    # get auth token
    auth_header = data.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                response_object = {
                    'code': 200,
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
            except Exception as e:
                response_object = {
                    'code': 200,
                    'status': 'fail',
                    'message': e
                }
        else:
            response_object = {
                'code': 401,
                'status': 'fail',
                'message': resp
            }
    else:
        response_object = {
            'code': 403,
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
    return response_object
