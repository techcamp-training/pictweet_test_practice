from django.test import TestCase
from django.core.exceptions import ValidationError
from .factories import CommentFactory

class CommentModelTestCase(TestCase):
    def setUp(self):
        self.comment = CommentFactory.build()

    def test_text_cannot_be_blank(self):
        """テキストが空の場合コメントの作成が失敗することをテスト"""
        self.comment.text = ''
        with self.assertRaises(ValidationError)as cm:
            self.comment.full_clean()

        self.assertIn('text', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['text'], ["このフィールドは空ではいけません。"])

    def test_comment_without_tweet(self):
        """ツイートが指定されていないコメントの作成が失敗することをテスト"""
        self.comment.tweet = None
        with self.assertRaises(ValidationError)as cm:
            self.comment.full_clean()

        self.assertIn('tweet', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['tweet'], ["このフィールドには NULL を指定できません。"])

    def test_comment_without_user(self):
        """ユーザーが指定されていないコメントの作成が失敗することをテスト"""
        self.comment.user = None
        with self.assertRaises(ValidationError)as cm:
            self.comment.full_clean()

        self.assertIn('user', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['user'], ["このフィールドには NULL を指定できません。"])