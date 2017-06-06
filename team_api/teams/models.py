from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        verbose_name=_('team'))


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
