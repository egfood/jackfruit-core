from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class GreenUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, is_active=True):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            is_active=is_active,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class GreenUser(AbstractUser):
    _profile = None

    email = models.EmailField('Email', unique=True)
    username = None

    objects = GreenUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def profile(self):
        if self._profile is None:
            profile_attr_names = ("buyer_buyerprofile", "farmer_farmerprofile")
            profile_was_find = False
            for attr_name in profile_attr_names:
                if hasattr(self, attr_name):
                    profile_was_find = True
                    self._profile = getattr(self, attr_name)
            if not profile_was_find:
                raise AttributeError("User profile not found!")

    def is_buyer(self):
        return self.profile.type == "BuyerProfile"

    def is_farmer(self):
        return self.profile.type == "FarmerProfile"