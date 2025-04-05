
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')), 
    path('', include('posts.urls')),    
    path('auth/', include('djoser.urls.jwt')),    # auth/jwt/refresh, auth/jwt/verify 
    path('auth/login', TokenObtainPairView.as_view(), name='login'),  # access to the token 
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refreshtoken'),

]
