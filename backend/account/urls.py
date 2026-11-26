from django.contrib import admin
from django.urls import include, path
from account import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("me/", views.me_view, name="me"),
    path("me/update/", views.me_update_view, name="me_update"),
    path("profile_list/", views.profile_list_view, name="profile_list"),
    path("delete_profile/<int:pk>/", views.delete_user_view, name="delete_profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
