from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import ugettext as _

from rest_framework import serializers


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
            user = get_user_model().objects.get(email=data['email'])
        except ObjectDoesNotExist:
            raise ValidationError(_('Invalid credentials.'))

        if not user.check_password(data['password']):
            raise ValidationError(_('Invalid credentials.'))

        return data
