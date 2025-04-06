from django.urls import path
from .views import (
    PostCreateView, PostDetailView, FollowUserView, UnfollowUserView, UserFollowingListView,
    UserPostView, UserPostDetail, 
)


urlpatterns = [
    path('post/create/', PostCreateView.as_view(), name='post-detail'),  # TO CREATE POST USING (POST), AND LIST OF ALL POSTS USING [GET] METHOD
    path('post/detail/<int:post_id>/', PostDetailView.as_view(), name='post-detail'), # TO UPDATE, DELETE, AND DETAIL VIEW POST RESPECTIVELY[PUT, DELETE, GET]



            #___URLS FOR FOLLOWERS (generics/apiview)
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/', UserFollowingListView.as_view(), name='user-following'),

           #___URLS FOR USERS (generics/apiview)
    path('user/<int:user_id>/posts/', UserPostView.as_view(), name='user-posts'),
    path('user/<int:user_id>/post/<int:post_id>/', UserPostDetail.as_view(), name='user-sepecific-order')
]