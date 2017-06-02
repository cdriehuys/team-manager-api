from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    """
    A team is made up of a collection of players.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'))

    def __str__(self):
        """
        Convert the instance to a string.

        Returns:
            The team's name.
        """
        return self.name
