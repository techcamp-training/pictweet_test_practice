from django.test import TestCase
from django.core.exceptions import ValidationError
from ..factories.users import UserFactory
from ..factories.tweets import TweetFactory
from ..factories.comments import CommentFactory
class BaseCommentModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.tweet = TweetFactory.create(user=self.user)
        self.comment = CommentFactory.build(user=self.user, tweet=self.tweet)

class CommentModelSuccessTestCase(BaseCommentModelTestCase):
    """正常系のテストケース"""
    def test_tweet_creation(self):
        """コメントを保存できる"""
        self.comment.full_clean()
        self.comment.save()
        self.assertIsNotNone(self.comment.id)  # 保存されたことを確認

class CommentModelFailureTestCase(BaseCommentModelTestCase):
    """異常系のテストケース"""
    def test_text_cannot_be_blank(self):
        """テキストが空では保存できない"""
        self.comment.text = ''
        with self.assertRaises(ValidationError)as cm:
            self.comment.full_clean()

        self.assertIn('text', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['text'], ["このフィールドは空ではいけません。"])

    def test_comment_without_tweet(self):
        """ツイートが紐付いていなければ投稿できない"""
        self.comment.tweet = None
        with self.assertRaises(ValidationError)as cm:
            self.comment.full_clean()

        self.assertIn('tweet', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['tweet'], ["このフィールドには NULL を指定できません。"])

    def test_comment_without_user(self):
        """ユーザーが紐付いていなければ投稿できない"""
        self.comment.user = None
        with self.assertRaises(ValidationError)as cm:
            self.comment.full_clean()

        self.assertIn('user', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['user'], ["このフィールドには NULL を指定できません。"])