from rest_framework.reverse import reverse

from teams import serializers


def test_serialize(serializer_context, team_factory):
    """
    Test serializing a team.
    """
    team = team_factory()
    serializer = serializers.TeamListSerializer(
        team,
        context=serializer_context)

    expected = {
        'name': team.name,
        'url': reverse(
            'teams:team-detail',
            kwargs={'pk': team.pk},
            request=serializer_context['request'])
    }

    assert serializer.data == expected
