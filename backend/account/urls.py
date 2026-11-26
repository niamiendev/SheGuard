from django.contrib import admin
from django.urls import include, path
from account import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("me/", views.me_view, name="me"),
    path("refresh/", views.refresh_view, name="refresh")
]
