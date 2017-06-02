from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import ugettext as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging a user in.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)

    def validate(self, data):
        """
        Validate the provided credentials.

        As a side effect, the validation also saves the user
        corresponding to the provided credentials so we don't have to
        look it up again.

        Args:
            data:
                A dictionary containing the credentials to validate.

        Returns:
            The validated data.

        Raises:
            ValidationError:
                if the provided credentials are invalid.
        """
        try:
            self.user = get_user_model().objects.get(email=data['email'])
        except ObjectDoesNotExist:
            raise ValidationError(_('Invalid credentials.'))

        if not self.user.check_password(data['password']):
            raise ValidationError(_('Invalid credentials.'))

        return data


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for auth tokens.
    """

    class Meta:
        fields = ('key',)
        model = Token
        read_only_fields = ('key',)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users.
    """

    class Meta:
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }
        fields = ('email', 'password')
        model = get_user_model()

    def create(self, validated_data):
        """
        Create a new user.

        Args:
            validated_data:
                The data to create a new user from.

        Returns:
            A new user instance.
        """
        return get_user_model().objects.create_user(**validated_data)
