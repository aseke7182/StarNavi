from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    pong, UserList, Registration, UserLogin, UserLogout, UserActivity
)

urlpatterns = [
    path('ping/', pong),
    path('users/', UserList.as_view()),
    path('signup/', Registration.as_view()),
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view()),
    path('refresh/', jwt_views.TokenRefreshView.as_view()),
    path('activity/', UserActivity.as_view())
]
