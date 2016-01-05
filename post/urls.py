from django.conf.urls import url
from rest_framework.authtoken import views
from post.views import DetailUpdatePost, ListCreatePost, DetailUpdateGoal, \
    ListCreateGoal, DetailUpdateComment, ListCreateComment, \
    DetailUpdateDestroyUserMessage, ListCreateUserMessage, \
    DetailUpdateDestroyGroupMessage, ListCreateGroupMessage, \
    ListCreateCommentLike, DetailUpdateDestroyCommentLike

urlpatterns = [
    url(r'^posts/(?P<pk>\d+)', DetailUpdatePost.as_view(),
        name='api_post_detail_update'),
    url(r'^posts/', ListCreatePost.as_view(), name='api_post_list'),
    url(r'^goals/(?P<pk>\d+)', DetailUpdateGoal.as_view(),
        name='api_goal_detail_update'),
    url(r'^goals/', ListCreateGoal.as_view(), name='api_goal_list'),
    url(r'^comments/(?P<pk>\d+)', DetailUpdateComment.as_view(),
        name='api_comment_detail_update'),
    url(r'^comments/', ListCreateComment.as_view(), name='api_comment_list'),
    url(r'^messages/user/(?P<pk>\d+)',
        DetailUpdateDestroyUserMessage.as_view(),
        name='api_user_message_detail_update'),
    url(r'^messages/user/', ListCreateUserMessage.as_view(),
        name='api_user_message_list'),
    url(r'^messages/group/(?P<pk>\d+)', DetailUpdateDestroyGroupMessage.as_view(),
        name='api_group_message_detail_update'),
    url(r'^messages/group/', ListCreateGroupMessage.as_view(),
        name='api_group_message_list'),
    url(r'^api-token-auth/', views.obtain_auth_token, name='token_auth'),
    url(r'^likes/comments/(?P<pk>\d+)', DetailUpdateDestroyCommentLike.as_view(),
        name='api_comment_likes_detail'),
    url(r'^likes/comments/', ListCreateCommentLike.as_view(),
        name='api_comment_likes_list'),
]