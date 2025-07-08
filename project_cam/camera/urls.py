from django.urls import path
from .views import register_view, login_view, logout_view, video_page, video_feed

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("video/", video_page, name="video"),
    path("video_feed/", video_feed, name="video_feed"),
]
