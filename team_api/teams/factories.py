import factory

from teams import models


class TeamFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating teams.
    """
    name = 'Test Team'

    class Meta:
        model = models.Team


class TeamInviteFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating team invites.
    """
    email = factory.Sequence(lambda n: 'test{n}@example.com'.format(n=n))
    invite_accept_url = 'http://example.com/invites'
    signup_url = 'http://example.com/signup'
    team = factory.SubFactory('teams.factories.TeamFactory')

    class Meta:
        model = models.TeamInvite


class TeamMemberFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating team members.
    """
    team = factory.SubFactory('teams.factories.TeamFactory')
    user = factory.SubFactory('rest_auth.factories.UserFactory')

    class Meta:
        model = models.TeamMember
