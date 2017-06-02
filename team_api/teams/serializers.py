from rest_framework import serializers

from teams import models


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Team model.
    """
    url = serializers.HyperlinkedIdentityField(view_name='teams:team-detail')

    class Meta:
        fields = ('url', 'name')
        model = models.Team

    def create(self, validated_data):
        """
        Create a new team.

        We also create an admin member of the team.

        Args:
            validated_data:
                The data to construct the team from.
            user:
                The user creating the team. This user will be assigned
                as an admin member of the new team.

        Returns:
            A new ``Team`` instance.
        """
        user = validated_data.pop('user')
        team = models.Team.objects.create(**validated_data)
        models.TeamMember.objects.create(
            is_admin=True,
            team=team,
            user=user)

        return team
