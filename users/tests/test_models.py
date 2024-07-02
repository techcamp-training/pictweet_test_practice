from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Tweet
from .factories import TweetFactory




class BaseTweetModelTestCase(TestCase):
    def setUp(self):
        """各テスト実行前にデータベースの状態をリセットする"""
        Tweet.objects.all().delete()



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

class TweetModelFailureTestCase(BaseTweetModelTestCase):
    """異常系のテストケース"""

    def test_tweet_without_text(self):
        """テキストがないツイートの作成が失敗することをテスト"""
        tweet = TweetFactory.build(text="")
        with self.assertRaises(ValidationError):
            tweet.full_clean()
            tweet.save()


    def test_tweet_without_user(self):
        """ユーザーが指定されていないツイートの作成が失敗することをテスト"""
        tweet = TweetFactory.build(text="Hello World")
        tweet.user = None
        with self.assertRaises(ValidationError):
            tweet.full_clean()
            tweet.save()