from django.conf.urls import url
from user.views import DetailUsers, ListCreateUsers, DetailTheme, ListTheme, \
    DetailGroup, ListGroup, DetailRank, ListRank, DetailAchievement, \
    ListAchievement, DetailProfile, ListProfile, DetailUpdateDestroyFriendship, \
    ListCreateFriendship, DetailEarned, ListEarned, DetailBadgeGift, \
    ListCreateBadgeGift

urlpatterns = [
    url(r'^users/(?P<pk>\d+)', DetailUsers.as_view(),
        name='api_user_detail'),
    url(r'^users/', ListCreateUsers.as_view(), name='api_user_list'),
    url(r'^themes/(?P<pk>\d+)', DetailTheme.as_view(),
        name='api_theme_detail'),
    url(r'^themes/', ListTheme.as_view(), name='api_theme_list'),
    url(r'^groups/(?P<pk>\d+)', DetailGroup.as_view(),
        name='api_group_detail'),
    url(r'^groups/', ListGroup.as_view(), name='api_group_list'),
    url(r'^ranks/(?P<pk>\d+)', DetailRank.as_view(),
        name='api_rank_detail'),
    url(r'^ranks/', ListRank.as_view(), name='api_rank_list'),
    url(r'^achievements/(?P<pk>\d+)', DetailAchievement.as_view(),
        name='api_achievement_detail'),
    url(r'^achievements/', ListAchievement.as_view(),
        name='api_achievement_list'),
    url(r'^profiles/(?P<pk>\d+)', DetailProfile.as_view(),
        name='api_profile_detail'),
    url(r'^profiles/', ListProfile.as_view(), name='api_profile_list'),
    url(r'^friends/(?P<pk>\d+)', DetailUpdateDestroyFriendship.as_view(),
        name='api_friendship_detail_destroy'),
    url(r'^friends/', ListCreateFriendship.as_view(),
        name='api_friendship_list_create'),
    url(r'^earned/(?P<pk>\d+)', DetailEarned.as_view(),
        name='api_earned_detail'),
    url(r'^earned/', ListEarned.as_view(), name='api_earned_list'),
    url(r'^gifts/(?P<pk>\d+)', DetailBadgeGift.as_view(),
        name='api_gift_detail'),
    url(r'^gifts/', ListCreateBadgeGift.as_view(), name='api_gift_list'),
]

