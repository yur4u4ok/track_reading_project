from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.auth.serializers import TokenPairSerializer
from apps.users.serializers import UserSerializer


class TokenPairView(TokenObtainPairView):
    """
    Login
    """
    serializer_class = TokenPairSerializer


class RegisterView(CreateAPIView):
    """
    Register
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
