from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_auth import serializers


class LoginView(generics.GenericAPIView):
    """
    View for obtaining auth tokens.
    """
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        """
        Obtain an authentication token.
        """
        serializer = self.get_serializer(data=request.POST)

        if serializer.is_valid():
            token, _ = Token.objects.get_or_create(user=serializer.user)
            token_serializer = serializers.TokenSerializer(token)

            return Response(token_serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED)


class RegistrationView(generics.CreateAPIView):
    """
    create:
    Register a new user.
    """
    model = get_user_model()
    serializer_class = serializers.UserSerializer
