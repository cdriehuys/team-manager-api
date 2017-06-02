import pytest

from rest_auth.serializers import UserSerializer


@pytest.mark.django_db
def test_save():
    """
    New users should be creatable by saving the serializer.
    """
    data = {
        'email': 'test@example.com',
        'password': 'foo',
    }

    serializer = UserSerializer(data=data)

    assert serializer.is_valid()

    user = serializer.save()

    assert user.email == data['email']
    assert user.check_password(data['password'])


def test_serialize(user_factory):
    """
    Test serializing a user.
    """
    user = user_factory()
    serializer = UserSerializer(user)

    expected = {
        'email': user.email,
    }

    assert serializer.data == expected
