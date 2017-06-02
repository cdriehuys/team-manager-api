from rest_framework import status

import pytest

from rest_auth import serializers
from rest_auth.views import LoginView


login_view = LoginView.as_view()


def test_post(api_rf, token_factory, user_factory):
    """
    If valid credentials are posted, a response containing the user's
    token should be returned.
    """
    data = {
        'email': 'test@example.com',
        'password': 'password',
    }

    user = user_factory(**data)
    token = token_factory(user=user)

    serializer = serializers.TokenSerializer(token)

    request = api_rf.post('/', data)
    response = login_view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


@pytest.mark.django_db
def test_post_invalid_credentials(api_rf):
    """
    If invalid credentials are sent, a response containing the
    serializer's validation errors should be returned.
    """
    data = {
        'email': 'test@example.com',
        'password': 'password',
    }

    serializer = serializers.LoginSerializer(data=data)
    assert not serializer.is_valid()

    request = api_rf.post('/', data)
    response = login_view(request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == serializer.errors
