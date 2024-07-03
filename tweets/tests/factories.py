# factories.py
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ..models import Tweet
from users.tests.factories import UserFactory
import os
class TweetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tweet

    user = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence')

    @factory.lazy_attribute
    def image(self):
        # テスト用の画像ファイルパスを指定
        image_path = os.path.join(settings.BASE_DIR, 'tweets/tests/media/sakura.jpg')
        with open(image_path, 'rb') as img:
            return SimpleUploadedFile(name='sakura.jpg', content=img.read(), content_type='image/jpeg')
