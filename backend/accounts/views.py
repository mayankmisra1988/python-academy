import logging
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle

from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login Successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": ProfileSerializer(
                    user,
                    context={"request": request},
                ).data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return (
            User.objects
            .select_related("profile")
            .get(id=self.request.user.id)
        )


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"]
        ):
            return Response(
                {"error": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            validate_password(
                serializer.validated_data["new_password"],
                user,
            )
        except DjangoValidationError as exc:
            raise DRFValidationError(
                {"new_password": list(exc.messages)}
            ) from exc
        user.set_password(
            serializer.validated_data["new_password"]
        )
        user.save(update_fields=["password"])

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        response_data = {
            "message": (
                "If an account exists with this email, "
                "a password reset link will be sent."
            )
        }

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user:
            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )
            token = default_token_generator.make_token(user)

            frontend_url = getattr(
                settings,
                "FRONTEND_URL",
                "http://localhost:3000",
            ).rstrip("/")

            reset_link = (
                f"{frontend_url}/reset-password/{uid}/{token}"
            )

            try:
                send_mail(
                    subject="Reset your Python Academy password",
                    message=(
                        "We received a request to reset your password.\n\n"
                        f"Open this link to reset it:\n{reset_link}\n\n"
                        "If you did not request this, ignore this email."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception:
                logger.exception(
                    "Password reset email could not be sent."
                )

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        user.set_password(
            serializer.validated_data["new_password"]
        )
        user.save(update_fields=["password"])

        return Response(
            {
                "message": (
                    "Password reset successfully. Please log in."
                )
            },
            status=status.HTTP_200_OK,
        )
