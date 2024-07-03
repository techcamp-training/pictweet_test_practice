import factory
from comments.models import Comment
from users.tests.factories import UserFactory
from tweets.tests.factories  import TweetFactory

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    tweet = factory.SubFactory(TweetFactory)