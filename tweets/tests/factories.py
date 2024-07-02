# factories.py
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ..models import Tweet
import os

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'techcamp2024')
    nickname = factory.Faker('name')  # ユーザーモデルに nickname があると仮定

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
