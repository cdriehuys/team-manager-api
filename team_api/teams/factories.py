import factory

from teams import models


class TeamFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating teams.
    """
    name = 'Test Team'

    class Meta:
        model = models.Team


class TeamMemberFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating team members.
    """
    team = factory.SubFactory('teams.factories.TeamFactory')
    user = factory.SubFactory('rest_auth.factories.UserFactory')

    class Meta:
        model = models.TeamMember
