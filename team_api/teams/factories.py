import factory

from teams import models


class TeamFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating teams.
    """
    name = 'Test Team'

    class Meta:
        model = models.Team
