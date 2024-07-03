from django.test import TestCase
from django.test.utils import override_settings
# from django.core.files.uploadedfile import SimpleUploadedFile
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
        self.tweet = TweetFactory.create()


    @classmethod
    def tearDownClass(cls):
        """全体のテストが終わった後に作成されたメディアファイルを削除する"""
        super().tearDownClass()
        if os.path.exists(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)

class TweetModelSuccessTestCase(BaseTweetModelTestCase):
    """正常系のテストケース"""

    def test_tweet_creation(self):
        """ツイートが正しく生成され、保存されるかをテスト"""
        self.tweet.full_clean()
        self.assertTrue(True)

    def test_tweet_with_text_only(self):
        """テキストのみを持つツイートが正しく生成され、保存されるかをテスト"""
        self.tweet.image = None
        self.tweet.full_clean()
        self.assertTrue(True)


class TweetModelFailureTestCase(BaseTweetModelTestCase):
    """異常系のテストケース"""

    def test_tweet_without_text(self):
        """テキストがないツイートの作成が失敗することをテスト"""
        self.tweet.text = ''
        with self.assertRaises(ValidationError) as cm:
            self.tweet.full_clean()
        self.assertIn('text', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['text'], ["このフィールドは空ではいけません。"])

    def test_tweet_text_too_long(self):
        """テキストが280文字を超える場合のバリデーションをテスト"""
        self.tweet.text = 'a' * 281
        with self.assertRaises(ValidationError) as cm:
            self.tweet.full_clean()
        self.assertIn('text', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['text'], ["テキストは280文字以内で入力してください。"])

    def test_tweet_without_user(self):
        """ユーザーが指定されていないコメントの作成が失敗することをテスト"""
        self.tweet.user = None
        with self.assertRaises(ValidationError) as cm:
            self.tweet.full_clean()
        self.assertIn('user', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['user'], ["このフィールドには NULL を指定できません。"])

    # def test_tweet_with_invalid_image_format(self):
    #     """不正な画像形式のツイートが失敗することをテスト"""
    #     invalid_image_path = os.path.join(settings.BASE_DIR, 'tweets/tests/media/invalid.txt')
    #     with open(invalid_image_path, 'rb') as img:
    #         tweet = TweetFactory.build(text="いい写真です",
    #                                    image=SimpleUploadedFile(name='invalid.txt', content=img.read(),
    #                                                             content_type='text/plain'))
    #     with self.assertRaises(ValidationError)as cm:
    #         self.tweet.full_clean()

    #     self.assertIn('image', cm.exception.message_dict)
    #     self.assertEqual(cm.exception.message_dict['image'], ["有効な画像ファイルをアップロードしてください。"])
