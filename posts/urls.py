from django.urls import path
from . import views


urlpatterns = [
    path('post/create/', views.PostCreateView.as_view(), name='post-detail'),  # TO CREATE POST USING (POST), AND LIST OF ALL POSTS USING [GET] METHOD
    path('post/detail/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail'), # TO UPDATE, DELETE, AND DETAIL VIEW POST RESPECTIVELY[PUT, DELETE, GET]
]