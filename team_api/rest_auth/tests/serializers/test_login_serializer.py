import pytest

from rest_auth.serializers import LoginSerializer


def test_validate_credentials(user_factory):
    """
    If valid credentials are provided, the serializer should validate.
    """
    data = {
        'email': 'test@example.com',
        'password': 'foo',
    }

    # Create a user with test credentials
    user = user_factory(**data)

    # Create a serializer with the same credentials
    serializer = LoginSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.user == user


@pytest.mark.django_db
def test_validate_invalid_credentials():
    """
    If invalid credentials are provided, a validation error should be
    raised.
    """
    data = {
        'email': 'test@example.com',
        'password': 'foo',
    }
    serializer = LoginSerializer(data=data)

    expected = ['Invalid credentials.']

    assert not serializer.is_valid()
    assert serializer.errors['non_field_errors'] == expected
