from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from rest_framework import serializers

from teams import models


class TeamInviteSerializer(serializers.ModelSerializer):
    """
    Serializer for the ``TeamInvite`` model.
    """
    class Meta:
        fields = ('id', 'email', 'invite_accept_url', 'signup_url', 'team')
        model = models.TeamInvite

    def create(self, validated_data):
        """
        Create a new invite and send out a notification.

        Args:
            validated_data:
                The data to construct the invite from.

        Returns:
            The created invite.

        Raises:
            ValidationError:
                If the invite's email and team are not unique together.
        """
        invite = super().create(validated_data)
        invite.send_notification()

        return invite

    def update(self, *args, **kwargs):
        """
        Prevent an update by raising a ``ValidationError``.

        Invites should not be mutable because then they could be
        different from what the user thinks they will be from the email
        notification they received.

        Raises:
            ValidationError
        """
        raise ValidationError(_('Team invitations cannot be edited.'))

    def validate(self, data):
        """
        Ensure that this invite does not mirror an existing team member.

        Args:
            data:
                The data passed to the serializer.

        Returns:
            The validated data.

        Raises:
            ValidationError:
                If the data mirrors a team member that already exists.
        """
        email = data.get('email')
        team = data.get('team')

        if models.TeamMember.objects.filter(
                team=team,
                user__email=email).exists():
            raise ValidationError(
                _('That person already exists on the current team.'),
                code='non_unique_invite')

        return data


class TeamMemberListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for listing instances of the ``TeamMember`` model.
    """
    member_type_name = serializers.CharField(source='get_member_type_display')
    name = serializers.CharField(source='user.get_short_name')

    class Meta:
        extra_kwargs = {
            'url': {
                'view_name': 'teams:member-detail',
            },
        }
        fields = ('name', 'url', 'member_type_name')
        model = models.TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for single instances of the ``TeamMember`` model.
    """
    member_type_name = serializers.CharField(
        read_only=True,
        source='get_member_type_display')
    name = serializers.CharField(
        read_only=True,
        source='user.get_short_name')
    team = serializers.HyperlinkedRelatedField(
        read_only=True,
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
    invites = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='teams:team-invites')
    members = TeamMemberListSerializer(
        many=True,
        read_only=True,
        required=False)

    class Meta:
        fields = ('name', 'invites', 'members')
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
