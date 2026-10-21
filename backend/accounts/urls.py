from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
)


urlpatterns = [
    # Authentication
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

    # JWT Refresh
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Profile
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    # Change Password
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),

    # Forgot Password
    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),

    # Reset Password
    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
]
