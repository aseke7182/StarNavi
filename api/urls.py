from django.urls import path

from .views import CreateListApiView, PostDetailApiView

urlpatterns = [
    path('posts/', CreateListApiView.as_view()),
    path('posts/<int:pk>/', PostDetailApiView.as_view()),
    # path('analytics/', LikeAnalytics.as_view()),
]
