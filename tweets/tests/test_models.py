from django.test import TestCase
from django.test.utils import override_settings
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

    #ここもいる？
    @classmethod
    def tearDownClass(cls):
        """全体のテストが終わった後に作成されたメディアファイルを削除する"""
        super().tearDownClass()
        if os.path.exists(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)

class TweetModelSuccessTestCase(BaseTweetModelTestCase):
    """正常系のテストケース"""

    def test_tweet_creation(self):
        """画像とテキストを投稿できる"""
        self.tweet.full_clean()
        self.assertTrue(True)

    def test_tweet_with_text_only(self):
        """テキストのみで投稿できる"""
        self.tweet.image = None
        self.tweet.full_clean()
        self.assertTrue(True)


class TweetModelFailureTestCase(BaseTweetModelTestCase):
    """異常系のテストケース"""

    def test_tweet_without_text(self):
        """テキストが空では投稿できない"""
        self.tweet.text = ''
        with self.assertRaises(ValidationError) as cm:
            self.tweet.full_clean()
        self.assertIn('text', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['text'], ["このフィールドは空ではいけません。"])

    def test_tweet_text_too_long(self):
        """テキストが280文字以下でないと投稿できない"""
        self.tweet.text = 'a' * 281
        with self.assertRaises(ValidationError) as cm:
            self.tweet.full_clean()
        self.assertIn('text', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['text'], ["テキストは280文字以内で入力してください。"])

    def test_tweet_without_user(self):
        """ユーザーが紐付いていなければ投稿できない"""
        self.tweet.user = None
        with self.assertRaises(ValidationError) as cm:
            self.tweet.full_clean()
        self.assertIn('user', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['user'], ["このフィールドには NULL を指定できません。"])