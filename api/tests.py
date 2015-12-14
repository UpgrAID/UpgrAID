from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from post.models import Goal, Comment
from post.models import Post
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

    # def test_post_list(self):
