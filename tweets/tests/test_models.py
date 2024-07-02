from django.test import TestCase
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from ..models import Tweet
from .factories import TweetFactory
import os
from django.conf import settings
import shutil

MEDIA_ROOT_TEST = os.path.join(settings.BASE_DIR, 'tweets/tests/media/images')

@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class BaseTweetModelTestCase(TestCase):
    def setUp(self):
        """各テスト実行前にデータベースの状態をリセットする"""
        Tweet.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        """全体のテストが終わった後に作成されたメディアファイルを削除する"""
        super().tearDownClass()
        if os.path.exists(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)

@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class TweetModelSuccessTestCase(BaseTweetModelTestCase):
    """正常系のテストケース"""

    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""
        saved_tweets = Tweet.objects.all()
        self.assertEqual(saved_tweets.count(), 0)

    def test_tweet_creation(self):
        """ツイートが正しく生成されるかをテスト"""
        tweet = TweetFactory()
        self.assertIsNotNone(tweet.pk)

    def test_tweet_with_text_only(self):
        """テキストのみを持つツイートが正しく生成されるかをテスト"""
        tweet = TweetFactory(image=None)
        self.assertIsNotNone(tweet.pk)

@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class TweetModelFailureTestCase(BaseTweetModelTestCase):
    """異常系のテストケース"""

    def test_tweet_without_text(self):
        """テキストがないツイートの作成が失敗することをテスト"""
        tweet = TweetFactory.build(text="")
        with self.assertRaises(ValidationError):
            tweet.full_clean()
            tweet.save()

    def test_tweet_text_too_long(self):
        """テキストが280文字を超える場合のバリデーションをテスト"""
        long_text = 'a' * 281  # 281文字のテキスト
        tweet = TweetFactory.build(text=long_text)
        with self.assertRaises(ValidationError):
            tweet.full_clean() #tweet.full_clean() だけでは、特定のデータベースレベルの制約がチェックされないことがある
            tweet.save() #テキストが280文字を超える場合のバリデーションはcleanに記載してあるのでsaveは行わなくても良い

    def test_tweet_without_user(self):
        """ユーザーが指定されていないツイートの作成が失敗することをテスト"""
        tweet = TweetFactory.build(text="Hello World")
        tweet.user = None
        with self.assertRaises(ValidationError):
            tweet.full_clean() #モデルに定義されたカスタムのバリデーションロジックを実行
            tweet.save()
            # 外部キーが正しく設定されているか（存在するユーザーが設定されているか）といったチェックはsave()メソッドで行われる

    # def test_tweet_with_invalid_image_format(self):
    #     """不正な画像形式のツイートが失敗することをテスト"""
    #     invalid_image_path = os.path.join(settings.BASE_DIR, 'tweets/tests/media/invalid.txt')
    #     with open(invalid_image_path, 'rb') as img:
    #         tweet = TweetFactory.build(text="いい写真です",
    #                                    image=SimpleUploadedFile(name='invalid.txt', content=img.read(),
    #                                                             content_type='text/plain'))
    #     with self.assertRaises(ValidationError):
    #         tweet.save()
