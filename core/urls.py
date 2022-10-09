from django.contrib import admin
from django.urls import path, re_path, include
from django.http import HttpResponse, response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # Djoser
    path('register/', include('djoser.urls')),
    re_path('^auth/', include('djoser.urls.authtoken')),
    # Messages
    re_path(r'api/', include('messageapp.urls')),
    # JWT
    path('jwt/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('jwt/token/verify', TokenVerifyView.as_view(), name="token_verify"),

    path(r'', include("messageapp.urls")),

]
