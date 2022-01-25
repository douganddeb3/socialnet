
from django.urls import path

from . import views

app_name = 'network'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("like/<int:pk>/", views.like, name="like"),
    path("unlike/<int:pk>/", views.unlike, name="unlike"),
    path("following/<int:pk>/", views.following, name="following"),
    path("unfollowing/<int:pk>/", views.unfollowing, name="unfollowing"),
    path("edit/<int:pk>/", views.edit, name="edit"),
]
