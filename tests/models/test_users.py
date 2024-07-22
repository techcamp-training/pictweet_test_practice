from django.test import TestCase
from django.core.exceptions import ValidationError
from ..factories.users import UserFactory


class BaseUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.build()
class UserModelSuccessTestCase(BaseUserModelTest):
    """正常系のテストケース"""
    def test_tweet_creation(self):
        """ユーザーの登録ができる"""
        self.user.full_clean()

class UserModelFailureTestCase(BaseUserModelTest):
    """異常系のテストケース"""
    def test_nickname_cannot_be_blank(self):
        """nicknameが空では登録できない"""
        self.user.nickname = ''

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('nickname', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['nickname'], ["このフィールドは空ではいけません。"])

    def test_email_cannot_be_blank(self):
        """emailが空では登録できない"""
        self.user.email = ''

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('email', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['email'], ["このフィールドは空ではいけません。"])

    def test_password_cannot_be_blank(self):
        """passwordは空では登録できない"""
        self.user.password = ''

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('password', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['password'], ["このフィールドは空ではいけません。"])

    def test_nickname_length_exceeds_limit(self):
        """nicknameが10文字より大きい場合は登録できない"""
        self.user.nickname = 'a' * 11

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('nickname', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['nickname'], ["この値は 10 文字以下でなければなりません( 11 文字になっています)。"])

    def test_unique_email_constraint(self):
        """重複したemailが存在する場合は登録できない"""
        self.user.save()
        another_user = UserFactory.build(email=self.user.email)
        with self.assertRaises(ValidationError) as cm:
            another_user.full_clean()
        self.assertIn('email', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['email'], ["この Email を持った Custom user が既に存在します。"])


    def test_email_must_contain_at_symbol(self):
        """emailは@を含まないと登録できない"""
        self.user.email = 'notanemail'

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('email', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['email'], ["有効なメールアドレスを入力してください。"])
