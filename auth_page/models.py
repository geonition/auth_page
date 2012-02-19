from django.contrib.auth.models import User
from django.db import models

class Email(models.Model):
    owner = models.ForeignKey(User,
                              related_name = 'owner')
    email = models.EmailField()
    email_is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40)