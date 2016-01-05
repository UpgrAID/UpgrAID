from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from post.models import Goal, Post, Comment
from rest_framework.test import APITestCase
from user.models import Theme


class PostTests(APITestCase):

    def setUp(self):
        self.user = User.object.create_user('test', email='test@test.com',
                                            password='testpassword')
        self.theme = Theme.objects.create(title='Test Theme')
        self.goal = Goal.objects.create(title='test goal', user=1, theme=1)
        self.post = Post.objects.create(title='test post',
                                        description='test description',
                                        user=1, goal=1)
        self.comment = Comment.objects.create(post=1,
                                              description='test comment',
                                              user=1)

    # def test_goal_list(self):
    #     url = reverse('api_goal_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_post_list(self):
    #     url = reverse('api_post_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_comment_list(self):
    #     url = reverse('api_comment_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_group_message_list(self):
    #     url = reverse('api_group_message_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_user_message_list(self):
    #     url = reverse('api_user_message_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_comment_like_list(self):
    #     url = reverse('api_comment_like_list_create')
    #     response = self.client.get(url, {}, format='json')