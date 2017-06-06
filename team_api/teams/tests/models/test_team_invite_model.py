from django.conf import settings
from django.core import mail
from django.db.utils import IntegrityError

import pytest

from teams import models


def test_create(team_factory):
    """
    Test creating a new team invitation.
    """
    models.TeamInvite.objects.create(
        email='test@example.com',
        invite_accept_url='example.com/invites',
        signup_url='example.com/signup',
        team=team_factory())


def test_get_notification_context(team_invite_factory):
    """
    This method should return the context used when rendering the
    invitation notification.
    """
    invite = team_invite_factory()

    expected = {
        'invite': invite,
        'team': invite.team,
    }

    assert invite._get_notification_context() == expected


def test_send_notification(team_invite_factory):
    """
    The ``send_notification`` method should send an email to the
    invite's ``email`` attribute notifying them of the invitation.
    """
    invite = team_invite_factory()

    assert invite.send_notification()
    assert len(mail.outbox) == 1

    msg = mail.outbox[0]

    assert msg.from_email == settings.DEFAULT_FROM_EMAIL
    assert msg.subject == "Invited to Join {team}".format(team=invite.team)
    assert msg.to == [invite.email]


def test_unique_email_and_team(team_invite_factory):
    """
    Invites should be unique with respect to email and team.
    """
    invite = team_invite_factory()

    with pytest.raises(IntegrityError):
        team_invite_factory(email=invite.email, team=invite.team)


def test_user_exists(team_invite_factory, user_factory):
    """
    If there is a user with the same email as the invite then the
    property should return ``True``.
    """
    user_factory(email='test@example.com')
    invite = team_invite_factory(email='test@example.com')

    assert invite.user_exists


def test_user_exists_no_user(team_invite_factory):
    """
    If there is no user with the given email address then the property
    should return ``False``.
    """
    invite = team_invite_factory()

    assert not invite.user_exists
