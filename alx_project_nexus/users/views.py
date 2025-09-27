from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

User = get_user_model()

@extend_schema(
    summary="Register a new user",
    description="Creates a new user account with email, password, and other required fields.",
    request=UserRegistrationSerializer,
    responses=UserRegistrationSerializer,
    tags=["Authentication"]
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


@extend_schema(
    summary="User login",
    description="Authenticates user and returns JWT access and refresh tokens.",
    request=CustomTokenObtainPairSerializer,
    responses=CustomTokenObtainPairSerializer,
    tags=["Authentication"]
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    