from django.db import models


class OneCTTN(models.Model):
    number = models.CharField(max_length=50)


class OneCTTNItem(models.Model):
    onec_ttn = models.ForeignKey(OneCTTN, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=1)
