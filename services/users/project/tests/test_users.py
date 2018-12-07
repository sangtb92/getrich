import json
import unittest

from project import db
from project.api.model.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Test for the Users Service."""

    def test_users_pingpong(self):
        """Ensure the /ping route behaves correctly."""
        res = self.client.get('/api/v1/users/ping')
        data = json.loads(res.data.decode())
        self.assertTrue(res.status_code, 200)

    def test_add_user(self):
        with self.client:
            response = self.client.post(
                '/api/v1/users/register',
                data=json.dumps({
                    'user_name': 'sangnd',
                    'd_name': 'Nguyen Sang',
                    'password': 'Ali33team@#',
                    'phone': '0985375631'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('message', data['message'])


if __name__ == '__main__':
    unittest.main()
    with open("a") as a:
        pass