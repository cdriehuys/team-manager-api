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

        password = kwargs.pop('password')

        user = manager.create(*args, **kwargs)
        user.set_password(password)
        user.save()

        return user
