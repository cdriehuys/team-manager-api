from django.contrib.auth import get_user_model

import pytest

from rest_framework import status

from rest_auth import serializers
from rest_auth.views import RegistrationView


registration_view = RegistrationView.as_view()


@pytest.mark.django_db
def test_register(api_rf):
    """
    POSTing a user's information should create a new user.
    """
    data = {
        'email': 'test@example.com',
        'password': 'foo',
    }

    serializer = serializers.UserSerializer(data=data)
    assert serializer.is_valid()

    request = api_rf.post('/', data)
    response = registration_view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == serializer.data

    user = get_user_model().objects.get(email=data['email'])
    assert user.check_password(data['password'])


def test_register_invalid(api_rf):
    """
    Submitting invalid data should display errors.
    """
    data = {
        'password': 'foo',
    }

    serializer = serializers.UserSerializer(data=data)
    assert not serializer.is_valid()

    request = api_rf.post('/', data)
    response = registration_view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == serializer.errors
