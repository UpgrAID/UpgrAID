from api.views import ListCreateUsers, DetailUsers, DetailUpdatePost, \
    ListCreatePost, DetailUpdateGoal, ListCreateGoal, DetailUpdateComment, \
    ListCreateComment, DetailTheme, ListTheme, DetailGroup, ListGroup, \
    DetailRank, ListRank, DetailAchievement, ListAchievement, ListCreateProfile, \
    DetailProfile
from django.conf.urls import url
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^users/(?P<pk>\d+)', DetailUsers.as_view(),
        name='api_user_detail'),
    url(r'^users/', ListCreateUsers.as_view(), name='api_user_list'),
    url(r'^posts/(?P<pk>\d+)', DetailUpdatePost.as_view(),
        name='api_post_detail_update'),
    url(r'^posts/', ListCreatePost.as_view(), name='api_post_list'),
    url(r'^goals/(?P<pk>\d+)', DetailUpdateGoal.as_view(),
        name='api_goal_detail_update'),
    url(r'^goals/', ListCreateGoal.as_view(), name='api_goal_list'),
    url(r'^comments/(?P<pk>\d+)', DetailUpdateComment.as_view(),
        name='api_comment_detail_update'),
    url(r'^comments/', ListCreateComment.as_view(), name='api_comment_list'),
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
    url(r'^achievements/', ListAchievement.as_view(), name='api_achievement_list'),
    url(r'^profiles/(?P<pk>\d+)', DetailProfile.as_view(),
        name='api_profile_detail'),
    url(r'^profiles/', ListCreateProfile.as_view(), name='api_profile_list'),
]