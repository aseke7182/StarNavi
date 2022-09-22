import datetime

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=255,
        unique=True,
    )
    admin = models.BooleanField(default=False)
    objects = UserManager()
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.admin
