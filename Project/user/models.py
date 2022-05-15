from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib import admin

LEVEL_ONE = 'F'
LEVEL_TWO = 'S'
LEVEL_THREE = 'T'

LEVEL_CHOICES = [
    (LEVEL_ONE, 'One'),
    (LEVEL_TWO, 'Two'),
    (LEVEL_THREE, 'Three'),
]


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
    ADMIN = 'A'
    STUDENT = 'S'
    PROFESSOR = 'P'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
    ]
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^(010|011|012|015)', message="Phone Number must be start with 012 or 015 or 010 or 011")
    phone = models.CharField(
        validators=[phone_regex], max_length=11, unique=True)
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
        ordering = ('-created_at', '-updated_at',)


class Professor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='professor')
    avatar = models.ImageField(
        default='professor/default.jfif', upload_to='professor', null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def phone(self):
        return self.user.phone

    @admin.display(ordering='user__email')
    def email(self):
        return self.user.email

    class Meta:
        ordering = ['user__email']


class Student(models.Model):
    level = models.CharField(
        max_length=1, choices=LEVEL_CHOICES, default=LEVEL_TWO)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def phone(self):
        return self.user.phone

    @admin.display(ordering='user__email')
    def email(self):
        return self.user.email

    class Meta:
        ordering = ['user__email']


class Group(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name='group')
    level = models.CharField(
        max_length=1, choices=LEVEL_CHOICES, default=LEVEL_TWO)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'professor'],


class Professor_Student(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'professor'],


class Professor_Level(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    level = models.CharField(
        max_length=1, choices=LEVEL_CHOICES, default=LEVEL_TWO)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['professor', 'level'],
        verbose_name = 'Professor Level',
        verbose_name_plural = 'Professor Levels'


class Request(models.Model):
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name='request')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['professor', 'student'],


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name='chapter')
    level = models.CharField(
        max_length=1, choices=LEVEL_CHOICES, default=LEVEL_TWO)
