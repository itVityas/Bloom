from django.db import models

from apps.shtrih.models import Models


class OneCTTN(models.Model):
    number = models.CharField(max_length=50)
    series = models.CharField(max_length=50, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        onec = OneCTTN.objects.filter(number=self.number, series=self.series).first()
        if onec:
            OneCTTNItem.objects.filter(onec_ttn=onec).delete()
            return None

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.number


class OneCTTNItem(models.Model):
    onec_ttn = models.ForeignKey(OneCTTN, on_delete=models.CASCADE)
    model = models.ForeignKey(Models, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    count = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name} ({self.count})"
