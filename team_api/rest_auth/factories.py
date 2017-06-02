import factory


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating users.
    """
    email = factory.sequence(lambda n: 'test{n}@example.com'.format(n=n))
    password = 'password'

    class Meta:
        model = 'rest_auth.User'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Create a new user and set a password for the user.
        """
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)
