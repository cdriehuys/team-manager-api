from rest_framework import serializers

from teams import models


class TeamMemberListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing instances of the ``TeamMember`` model.
    """
    member_type_name = serializers.CharField(source='get_member_type_display')
    name = serializers.CharField(source='user.get_short_name')

    class Meta:
        fields = ('name', 'member_type_name')
        model = models.TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for single instances of the ``TeamMember`` model.
    """
    member_type_name = serializers.CharField(source='get_member_type_display')
    name = serializers.CharField(source='user.get_short_name')
    team = serializers.HyperlinkedRelatedField(
        queryset=models.Team.objects.all(),
        view_name='teams:team-detail')

    class Meta:
        fields = (
            'name', 'team', 'member_type', 'member_type_name', 'is_admin'
        )
        model = models.TeamMember


class TeamListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple teams.
    """
    url = serializers.HyperlinkedIdentityField(view_name='teams:team-detail')

    class Meta:
        fields = ('name', 'url')
        model = models.Team


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.
    """
    members = TeamMemberListSerializer(
        many=True,
        read_only=True,
        required=False)

    class Meta:
        fields = ('name', 'members')
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
