from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import CustomUser

class UserModelTest(TestCase):
    def test_nickname_cannot_be_blank(self):
        user = CustomUser(nickname='', email='test123@test.com', password='techcamp2024')

        with self.assertRaises(ValidationError) as cm:
            user.full_clean()

        self.assertIn('nickname', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['nickname'], ["このフィールドは空ではいけません。"])

    def test_password_cannot_be_blank(self):
        user = CustomUser(nickname='abe', email='test123@test.com', password='')

        with self.assertRaises(ValidationError) as cm:
            user.full_clean()

        self.assertIn('password', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['password'], ["このフィールドは空ではいけません。"])
