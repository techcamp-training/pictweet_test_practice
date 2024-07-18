import factory
from comments.models import Comment

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('sentence')