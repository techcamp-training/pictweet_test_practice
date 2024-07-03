from django.test import TestCase
from django.core.exceptions import ValidationError
from .factories import UserFactory

class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory.build()


    def test_nickname_cannot_be_blank(self):
        self.user.nickname = ''

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('nickname', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['nickname'], ["このフィールドは空ではいけません。"])

    def test_email_cannot_be_blank(self):
        self.user.email = ''

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('email', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['email'], ["このフィールドは空ではいけません。"])