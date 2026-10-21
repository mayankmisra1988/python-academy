import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

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
                api_key = settings.RESEND_API_KEY

                if not api_key:
                    logger.error(
                        "Password reset email failed: "
                        "RESEND_API_KEY is not configured."
                    )
                else:
                    email_data = {
                        "from": settings.RESEND_FROM_EMAIL,
                        "to": [user.email],
                        "subject": (
                            "Reset your Python Academy password"
                        ),
                        "text": (
                            "We received a request to reset your password.\n\n"
                            f"Open this link to reset it:\n{reset_link}\n\n"
                            "If you did not request this, ignore this email."
                        ),
                    }

                    api_request = urllib.request.Request(
                        "https://api.resend.com/emails",
                        data=json.dumps(email_data).encode("utf-8"),
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json",
                            "User-Agent": "PythonAcademy/1.0",
                        },
                        method="POST",
                    )

                    with urllib.request.urlopen(
                        api_request,
                        timeout=10,
                    ) as api_response:
                        if api_response.status in (200, 201, 202):
                            logger.info(
                                "Password reset email accepted by Resend."
                            )
                        else:
                            logger.error(
                                "Resend API returned HTTP %s.",
                                api_response.status,
                            )

            except urllib.error.HTTPError as exc:
                error_body = exc.read().decode(
                    "utf-8",
                    errors="replace",
                )
                logger.error(
                    "Resend API rejected password reset email: "
                    "HTTP %s; response: %s",
                    exc.code,
                    error_body[:1000],
                )
            except Exception:
                logger.exception(
                    "Password reset email could not be sent through Resend."
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
