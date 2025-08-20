from email.policy import default
from enum import unique
from wsgiref.validate import validator

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not mobile:
            raise ValueError("Mobile number must be provided")

        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Set is_superuser True")

        return self.create_user(email, mobile, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile_regex = RegexValidator(regex=r'^[6-9]\d{9}$', message="Enter a valid 10 dig")
    mobile = models.CharField(validators=[mobile_regex], max_length=10, unique=True)

    full_name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile", "full_name"]

    def __str__(self):
        return f"{self.email} ({self.mobile})"