from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class GreenUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, is_active=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name
        )

        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, is_active=True):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            is_active=is_active,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class GreenUser(AbstractUser):
    email = models.EmailField('Email', unique=True)
    username = None

    objects = GreenUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]