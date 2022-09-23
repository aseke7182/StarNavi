import time

from django.test import Client
from django.test import TestCase

from .messages import logout_msg
from .models import User


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(name='askar', surname='musaev', username='aseke7182')
        self.user.set_password('password')
        self.user.save()

    def test_user_list(self):
        response = self.client.get('/auth/users/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_registration(self):
        response = self.client.post('/auth/signup/', {
            'name': 'test_name',
            'surname': 'test_surname',
            'username': 'test_username',
            'password': 'test_password'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'test_name')
        self.assertEqual(response.json()['username'], 'test_username')

        response = self.client.get('/auth/users/')
        self.assertEqual(len(response.json()), 2)

    def test_auth(self):
        # Login
        response = self.client.post('/auth/login/', {
            'username': 'aseke7182',
            'password': 'password'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual('access' in response.json(), True)
        self.assertEqual('refresh' in response.json(), True)

        # Log out
        access_token = response.json()['access']
        refresh_token = response.json()['refresh']
        header = {'HTTP_AUTHORIZATION': 'Bearer ' + access_token}
        logout = self.client.post('/auth/logout/', **header)

        self.assertEqual(logout.status_code, 200)
        self.assertEqual(logout.json()['detail'], logout_msg)

        # Refresh tokens
        refresh = self.client.post('/auth/refresh/', {
            'refresh': refresh_token
        })

        self.assertEqual(refresh.status_code, 200)
        self.assertEqual('access' in refresh.json(), True)
        self.assertEqual('refresh' in refresh.json(), True)

    def test_activity(self):
        # No activity/login yet
        user = self.user
        self.assertIsNone(user.last_login)
        self.assertIsNone(user.last_activity)

        login = self.client.post('/auth/login/', {
            'username': 'aseke7182',
            'password': 'password'
        })
        header = {'HTTP_AUTHORIZATION': 'Bearer ' + login.json()['access']}

        time.sleep(2)
        self.client.post('/api/posts/', {
            'content': 'test_content'
        }, **header)

        user = self.client.get('/auth/activity/', **header)

        self.assertEqual(user.status_code, 200)
        self.assertIsNotNone(user.json()['last_login'])
        self.assertIsNotNone(user.json()['last_activity'])
        self.assertNotEqual(user.json()['last_activity'], user.json()['last_login'])
