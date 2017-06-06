from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext, ugettext_lazy as _


class Team(models.Model):
    """
    A team is made up of a collection of players.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))

    def __str__(self):
        """
        Convert the instance to a string.

        Returns:
            The team's name.
        """
        return self.name


class TeamInvite(models.Model):
    """
    An invitation to join a team.
    """
    email = models.EmailField(verbose_name=_('email'))
    invite_accept_url = models.URLField(
        help_text=_('The URL where the user can go to accept the invitation.'),
        verbose_name=_('invite accept URL'))
    signup_url = models.URLField(
        help_text=_('The URL where the user can go to sign up for an '
                    'account.'),
        verbose_name=_('signup url'))
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        verbose_name=_('team'))

    class Meta:
        unique_together = ('email', 'team')

    @property
    def user_exists(self):
        """
        Determine if there is a user with the invite's email.
        """
        return get_user_model().objects.filter(email=self.email).exists()

    def accept(self, user):
        """
        Accept the invitation.

        Creates a new team member linking the invite's team and the
        specified user.

        Args:
            user:
                The user accepting the invitation.
        """
        TeamMember.objects.create(team=self.team, user=user)

        self.delete()

    def send_notification(self):
        """
        Send an email notification about the invite.

        Returns:
            ``True`` if the email was successfully sent and ``False``
            otherwise.
        """
        subject = ugettext('Invited to Join %(team)s' % {
            'team': self.team.name
        })
        message = render_to_string(
            'teams/email/invite.txt',
            self._get_notification_context())

        return bool(mail.send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=message,
            recipient_list=[self.email],
            subject=subject))

    def _get_notification_context(self):
        """
        Get context data to use when sending a notification email.

        Returns:
            A dictionary containing context for the notification email.
        """
        return {
            'invite': self,
            'team': self.team,
        }


class TeamMember(models.Model):
    """
    A team member is a link between a user and a team.

    The model also contains information about what type of relationship
    the team and user have, i.e. player or coach.
    """
    COACH = 0
    PLAYER = 1

    MEMBER_TYPE_CHOICES = (
        (COACH, _('Coach')),
        (PLAYER, _('Player')),
    )

    is_admin = models.BooleanField(
        default=False,
        help_text=_("Admin members are allowed to edit the team's "
                    "information, as well as change player info."),
        verbose_name=_('is admin'))
    member_type = models.PositiveSmallIntegerField(
        choices=MEMBER_TYPE_CHOICES,
        default=PLAYER,
        verbose_name=_('member type'))
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_('team'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'))
