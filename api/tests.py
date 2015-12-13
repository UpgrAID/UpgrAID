# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
# from rest_framework.test import APITestCase
# from user.models import Theme
#
#
# class PostTests(APITestCase):
#
#     def setUp(self):
#         self.user = User.object.create_user('test', email='test@test.com',
#                                             password='testpassword')
#         self.theme = Theme.objects.create(title='TestTheme')
#         self.goal = Goal.objects.create()
#         self.post = Post.objects.create()
#
#     def test_post_list