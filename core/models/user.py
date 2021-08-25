from functools import cached_property
from importlib import import_module

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models.base import ClassData


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

    email = models.EmailField('Email', unique=True)
    username = None
    first_name = None
    last_name = None

    objects = GreenUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    BUYER_PROFILE = ClassData("apps.buyer.models", "BuyerProfile")
    FARMER_PROFILE = ClassData("apps.farmer.models", "FarmerProfile")

    @cached_property
    def profile(self):
        profile_attr_names = ("buyer_buyerprofile", "farmer_farmerprofile")
        profile = None
        for attr_name in profile_attr_names:
            if hasattr(self, attr_name):
                profile = getattr(self, attr_name)
        if profile is None:
            raise AttributeError("User profile not found!")
        return profile

    @cached_property
    def is_buyer(self):
        return self.profile.type == self.BUYER_PROFILE.class_name

    @cached_property
    def is_farmer(self):
        return self.profile.type == self.FARMER_PROFILE.class_name

    @staticmethod
    def get_or_create_profile(user, profile_class_data: ClassData):
        try:
            return user.profile
        except AttributeError:
            module = import_module(profile_class_data.path_to_class)
            profile_model = getattr(module, profile_class_data.class_name)
            return profile_model()
