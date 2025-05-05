from django.db import models

from apps.account.models import User


class Visits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user id
    label = models.CharField(max_length=50)  # russian name
    url = models.CharField(max_length=250)   # visit url
