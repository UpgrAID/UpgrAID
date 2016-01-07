from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import Theme, Achievement, BadgeGift, Friendship, Rank


class PostTests(APITestCase):

    def setUp(self):
        self.rank = Rank.objects.create(title='Novice 5', exp_required=15)
        self.user = User.objects.create_user('test', email='test@test.com',
                                            password='testpassword')
        self.user2 = User.objects.create_user('test2', email='test2@test.com',
                                            password='test2password')
        self.user3 = User.objects.create_user('test3', email='test3@test.com',
                                            password='test3password')
        self.theme = Theme.objects.create(title='Test Theme')
        self.post_achievement = Achievement.objects.create(name='test achievement',
                                                           type='Post',
                                                           required_amount=1)
        self.friends = Friendship.objects.create(from_friend=self.user,
                                                 to_friend=self.user2)
        self.badge_gift = BadgeGift.objects.create(sender=self.user,
                                                   receiver=self.user2,
                                                   amount=1)

    def test_theme_list(self):
        url = reverse('api_theme_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_list(self):
        url = reverse('api_group_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rank_list(self):
        url = reverse('api_rank_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_achievement_list(self):
        url = reverse('api_achievement_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_friendship_list(self):
        url = reverse('api_friendship_list_create')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_friendship_create(self):
        url = reverse('api_friendship_list_create')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"from_friend": self.user.pk,
                                          "to_friend": self.user3.pk},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 2)
        self.assertEqual(self.user.friend_set.count(), 2)
        self.assertEqual(self.user2.to_friend_set.count(), 1)
        self.assertEqual(self.user3.to_friend_set.count(), 1)

    def test_earned_list(self):
        url = reverse('api_earned_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_badge_gift_list(self):
        url = reverse('api_gift_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_badge_gift_create(self):
        url = reverse('api_gift_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"receiver": self.user3.pk, "amount": 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)