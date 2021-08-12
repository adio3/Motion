from django.urls import path
from .views import ListCreatePostsView, ToggleLikeView, GetUpdateDeletePostView, ListLikedView, GetPostByUserIdView, \
    GetPostsFromFollowingView, GetPostsFromFriendsView, SearchPostsView

urlpatterns = [
    path('', ListCreatePostsView.as_view()),
    path('search', SearchPostsView.as_view()),
    path('<int:pk>/', GetUpdateDeletePostView.as_view()),
    path('following/', GetPostsFromFollowingView.as_view()),
    path('friends/', GetPostsFromFriendsView.as_view()),
    path('user/<int:user_id>/', GetPostByUserIdView.as_view()),
    path('toggle-like/<int:post_id>/', ToggleLikeView.as_view()),
    path('likes/', ListLikedView.as_view()),
]