from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        attrs["user"] = user
        return attrs


# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "email",
#             "username",
#             "first_name",
#             "last_name",
#             "role",
#             "phone",
#             "bio",
#             "profile_image",
#             "date_of_birth",
#             "is_verified",
#         )
#         read_only_fields = (
#             "id",
#             "email",
#             "role",
#             "is_verified",
#         )

class ProfileSerializer(serializers.ModelSerializer):

    learning_streak = serializers.IntegerField(
        source="profile.learning_streak",
        read_only=True,
    )

    completed_courses = serializers.IntegerField(
        source="profile.completed_courses",
        read_only=True,
    )

    total_certificates = serializers.IntegerField(
        source="profile.total_certificates",
        read_only=True,
    )

    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "phone",
            "bio",
            "profile_image",
            "date_of_birth",
            "is_verified",

            # Profile model fields
            "learning_streak",
            "completed_courses",
            "total_certificates",
        )

        read_only_fields = (
            "id",
            "email",
            "role",
            "is_verified",
            "learning_streak",
            "completed_courses",
            "total_certificates",
        )
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    new_password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True,
    )

    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        return attrs