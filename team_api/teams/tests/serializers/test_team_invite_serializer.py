from django.core import mail
from django.core.exceptions import ValidationError

import pytest

from teams import serializers


def test_create(team_factory):
    """
    The serializer should be able to create a new invite by saving valid
    data.
    """
    team = team_factory()
    data = {
        'email': 'test@example.com',
        'invite_accept_url': 'http://example.com/invites',
        'signup_url': 'http://example.com/signup',
        'team': team.pk,
    }

    serializer = serializers.TeamInviteSerializer(data=data)

    assert serializer.is_valid()

    invite = serializer.save()

    assert invite.email == data['email']
    assert invite.invite_accept_url == data['invite_accept_url']
    assert invite.signup_url == data['signup_url']
    assert invite.team == team

    assert len(mail.outbox) == 1


def test_create_non_unique(team_invite_factory):
    """
    The serializer should not validate if we attempt to save a non-
    unique invite.
    """
    invite = team_invite_factory()
    data = {
        'email': invite.email,
        'invite_accept_url': 'http://example.com/invites',
        'signup_url': 'http://example.com/signup',
        'team': invite.team.pk,
    }

    serializer = serializers.TeamInviteSerializer(data=data)
    assert not serializer.is_valid()


def test_serialize(team_invite_factory):
    """
    Test serializing a team invitation.
    """
    invite = team_invite_factory()
    serializer = serializers.TeamInviteSerializer(invite)

    expected = {
        'id': invite.id,
        'email': invite.email,
        'invite_accept_url': invite.invite_accept_url,
        'signup_url': invite.signup_url,
        'team': invite.team.pk,
    }

    assert serializer.data == expected


def test_update(team_factory, team_invite_factory):
    """
    Attempting to update a team invitation should raise a validation
    error.
    """
    invite = team_invite_factory()

    data = {
        'id': invite.id,
        'email': 'new@example.com',
        'invite_accept_url': 'http://example.com/invites2',
        'signup_url': 'http://example.com/signup2',
        'team': invite.team.pk,
    }

    serializer = serializers.TeamInviteSerializer(invite, data=data)

    assert serializer.is_valid()

    with pytest.raises(ValidationError):
        serializer.save()


def test_validate_existing_member(team_member_factory):
    """
    An invite that mirrors an existing user should not be valid.

    Regression test for #14
    """
    member = team_member_factory()
    data = {
        'email': member.user.email,
        'invite_accept_url': 'http://example.com/invites',
        'signup_url': 'http://example.com',
        'team': member.team.pk,
    }

    serializer = serializers.TeamInviteSerializer(data=data)

    assert not serializer.is_valid()
