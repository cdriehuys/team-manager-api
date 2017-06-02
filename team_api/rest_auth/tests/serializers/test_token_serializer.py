from rest_auth.serializers import TokenSerializer


def test_serialize(token_factory):
    """
    Test serializing a token.
    """
    token = token_factory()

    serializer = TokenSerializer(token)

    expected = {
        'key': token.key,
    }

    assert serializer.data == expected
