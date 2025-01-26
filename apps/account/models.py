from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .account_manager import AccountManager


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    username = models.CharField(db_index=True, max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    objects = AccountManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self.__generate_jwt_token()


class UserRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'role')
