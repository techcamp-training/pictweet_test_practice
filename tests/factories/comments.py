import factory
from comments.models import Comment
from .users import UserFactory
from .tweets  import TweetFactory

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    tweet = factory.SubFactory(TweetFactory)