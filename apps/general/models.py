from django.db import models
from rest_framework.exceptions import ValidationError

from apps.account.models import User


class Visits(models.Model):
    """
    Tracks user visits to different URLs within the application.

    Attributes:
        user (ForeignKey): Reference to the User who made the visit
        label (CharField): Descriptive name for the visited page (in Russian)
        url (CharField): The actual URL that was visited
        created_at (DateTimeField): Automatic timestamp of when the visit was recorded
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user id
    label = models.CharField(max_length=50)  # russian name
    url = models.CharField(max_length=250)   # visit url

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.email} visited {self.label}'


class AddTitle(models.Model):
    """
    Stores titles for additional content sections.

    Attributes:
        name (CharField): The title text
        created_at (DateTimeField): Automatic creation timestamp
        updated_at (DateTimeField): Automatic update timestamp
    """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class AddBody(models.Model):
    """
    Stores body content associated with AdditionalTitle.

    Attributes:
        body (TextField): The main content text
        title (ForeignKey): Reference to the associated AdditionalTitle
        created_at (DateTimeField): Automatic creation timestamp
        updated_at (DateTimeField): Automatic update timestamp
    """
    body = models.TextField()
    title = models.ForeignKey(AddTitle, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'Content for {self.title.name}'


class SiteLockManager(models.Manager):
    """Manager для работы с singleton записью"""

    def get_singleton(self):
        """Возвращает единственную запись или создает ее"""
        obj, created = self.get_or_create(pk=1)
        return obj

    def update_lock(self, **kwargs):
        """Обновляет настройки блокировки"""
        obj = self.get_singleton()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj


class SiteLock(models.Model):
    declare = models.BooleanField(default=False)
    decl_invoice = models.BooleanField(default=False)
    decl_upload = models.BooleanField(default=False)
    sgp = models.BooleanField(default=False)
    sez = models.BooleanField(default=False)
    sez_calc = models.BooleanField(default=False)
    sez_dbf_download = models.BooleanField(default=False)

    objects = SiteLockManager()

    def save(self, *args, **kwargs):
        """Разрешаем только одну запись"""
        if not self.pk and SiteLock.objects.exists():
            raise ValidationError('Может существовать только одна запись SiteLock')

        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Запрещаем удаление singleton записи"""
        raise ValidationError('Нельзя удалить запись SiteLock')

    def __str__(self):
        return 'Настройки блокировки сайта'
