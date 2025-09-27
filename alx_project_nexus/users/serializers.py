from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        help_text="User's email address. Must be unique.",
    )
    username = serializers.CharField(
        help_text="Username for the account. Must be unique.",
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Password for the account. Will be securely hashed.",
    )

    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Use email instead of username for JWT login"""
    username_field = "email"