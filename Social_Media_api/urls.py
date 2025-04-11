
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


...
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Social Media API",
      default_version='v1',
      description="A REST API for social media service",
      contact=openapi.Contact(email="nahombelayneh387@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', TokenObtainPairView.as_view(), name='login'),  # access to the token 
    path('api/', include('accounts.urls')), 
    path('', include('posts.urls')),    
    path('auth/', include('djoser.urls.jwt')),    # auth/jwt/refresh, auth/jwt/verify 
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refreshtoken'),

   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
