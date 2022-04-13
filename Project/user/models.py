from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib import admin


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, phone, password=None, **extra_fields):
        values = [email, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Admin must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Admin must have is_staff=True.')
        return self._create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'Admin'
    STUDENT = 'Student'
    PROFESSOR = 'Professor'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    ]
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^(010|011|012|015)', message="Phone Number must be start with 012 or 015 or 010 or 011")
    phone = models.CharField(validators=[
        RegexValidator('^(010|011|012|015)[0-9]{8}$', message='Phone Number must be start with 012 or 015 or 010 or 011'), ], max_length=11, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


    class Meta:
        ordering = ('-created_at', '-updated_at', )
