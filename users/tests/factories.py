import factory
from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Faker('email')
    nickname = factory.Faker('lexify', text='??????')
    password = factory.PostGenerationMethodCall('set_password', 'techcamp2024')