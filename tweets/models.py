from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
# from PIL import Image
import logging

# ログ設定
logger = logging.getLogger(__name__)
class Tweet(models.Model):
  class Meta:
    db_table = 'tweets'

  text = models.TextField(null=False)
  image = models.ImageField(upload_to='images/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)


  def clean(self):
          if not self.text:
              raise ValidationError({'text': 'このフィールドは空ではいけません。'})
          if len(self.text) > 280:
              raise ValidationError({'text': 'テキストは280文字以内で入力してください。'})