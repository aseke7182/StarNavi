from datetime import datetime

from django.test import Client
from django.test import TestCase

from auth_.models import User
from .models import Post, UserPostLike


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(name='askar', surname='musaev', username='aseke7182')
        self.user2 = User.objects.create(name='assyl', surname='suleiman', username='as2403')
        self.user.set_password('password')
        self.user2.set_password('password')
        self.user.save()
        self.user2.save()
        self.post = Post.objects.create(content='first publication', author_id=self.user.id)

    def test_post_creation(self):
        post = self.client.post('/api/posts/', {
            'content': 'test_content'
        })

        self.assertEqual(post.status_code, 401)

        login = self.client.post('/auth/login/', {
            'username': 'aseke7182',
            'password': 'password'
        })
        header = {'HTTP_AUTHORIZATION': 'Bearer ' + login.json()['access']}
        post_with_header = self.client.post('/api/posts/', {
            'content': 'test_content'
        }, **header)

        self.assertEqual(post_with_header.status_code, 201)
        posts_count = Post.objects.all().count()
        self.assertEqual(posts_count, 2)

    def test_like_post(self):
        login = self.client.post('/auth/login/', {
            'username': 'aseke7182',
            'password': 'password'
        })

        login2 = self.client.post('/auth/login/', {
            'username': 'as2403',
            'password': 'password'
        })

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + login.json()['access']}
        header2 = {'HTTP_AUTHORIZATION': 'Bearer ' + login2.json()['access']}

        # Invalid value for post like
        like_wrong = self.client.post('/api/posts/1/', {
            'value': 10
        }, **header)
        self.assertEqual(like_wrong.status_code, 404)

        post_id = Post.objects.last().id
        # First user like
        like = self.client.post(f'/api/posts/{post_id}/', {
            'value': 1
        }, **header)
        self.assertEqual(like.status_code, 200)

        post_like_count = Post.objects.get(id=post_id).likes
        self.assertEqual(post_like_count, 1)

        # Second user like
        self.client.post(f'/api/posts/{post_id}/', {
            'value': 1
        }, **header2)
        post_like_count = Post.objects.get(id=post_id).likes
        self.assertEqual(post_like_count, 2)

        # First user dislike
        self.client.post(f'/api/posts/{post_id}/', {
            'value': -1
        }, **header)
        post_like_count = Post.objects.get(id=post_id).likes
        self.assertEqual(post_like_count, 0)

        # First user dislike retrieve
        self.client.post(f'/api/posts/{post_id}/', {
            'value': 0
        }, **header)
        post_like_count = Post.objects.get(id=post_id).likes
        self.assertEqual(post_like_count, 1)

    def test_analytics(self):
        date1 = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        date2 = datetime.strptime('Jun 1 2022  1:33PM', '%b %d %Y %I:%M%p')
        UserPostLike.objects.create(user=self.user, post=self.post, value=1, updated_at=date1)
        UserPostLike.objects.create(user=self.user2, post=self.post, value=-1, updated_at=date2)
        like_count = UserPostLike.objects.count()
        login = self.client.post('/auth/login/', {
            'username': 'aseke7182',
            'password': 'password'
        })
        header = {'HTTP_AUTHORIZATION': 'Bearer ' + login.json()['access']}

        self.assertEqual(like_count, 2)
        analytics = self.client.get('/api/analytics/?date_from=14.09.2021&date_to=14.09.2023', **header)
        likes = analytics.json()['likes']
        dislikes = analytics.json()['dislikes']
        self.assertEqual(likes, 1)
        self.assertEqual(dislikes, 1)
