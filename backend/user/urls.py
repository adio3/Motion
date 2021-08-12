from django.urls import path
from user.views import ListAllUsers,ListUserProfileInfo,RetrieveUserProfile,ToggleFollowUserView, \
    ListFollowers, ListFollowees, SendFriendRequest, ListUpdateDeleteFriendRequest, ListAllFriends

urlpatterns = [
    path('users/', ListAllUsers.as_view()),
    path('users/me/',ListUserProfileInfo.as_view()),
    path('users/<int:user_id>/',RetrieveUserProfile.as_view()),
    path('social/followers/toggle-follow/<int:user_id>/',ToggleFollowUserView.as_view()),
    path('social/followers/',ListFollowers.as_view()),
    path('social/followees/',ListFollowees.as_view()),
    path('social/friends/',ListAllFriends.as_view()),
    path('social/friends/request/<int:user_id>/',SendFriendRequest.as_view()),
    path('social/friends/requests/<int:friend_request_id>/', ListUpdateDeleteFriendRequest.as_view()),
]