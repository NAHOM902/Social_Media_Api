from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)





urlpatterns = [

    path('register/', views.RegisterViews.as_view(), name='register'),
   
 ]