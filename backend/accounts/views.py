from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
)


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
                context={"request": request}
                ).data
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

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = request.user

        if not user.check_password(
            serializer.validated_data["old_password"]
        ):

            return Response(
                {
                    "error":
                    "Old password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        validate_password(
            serializer.validated_data["new_password"],
            user
        )

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save()

        return Response(
            {
                "message":
                "Password changed successfully."
            }
        )