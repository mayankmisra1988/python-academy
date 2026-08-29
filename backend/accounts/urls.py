from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
)


urlpatterns = [

    # =========================
    # AUTHENTICATION
    # =========================

    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    # =========================
    # JWT REFRESH
    # =========================

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # =========================
    # PROFILE
    # =========================

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    # =========================
    # CHANGE PASSWORD
    # =========================

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
]