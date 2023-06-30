from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password 


class ProfileManager(BaseUserManager):
    def create_user(self, user_name, user_contact, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('The Email field must be set')
        hashed_pwd = make_password(password, salt=None)
        user = self.model(
            user_name=user_name,
            user_contact=user_contact,
            password=hashed_pwd,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, user_contact, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('The Email field must be set')
        user = self.create_user(
            user_name=user_name,
            user_contact=user_contact,
            email=email,
            password=password,
            **extra_fields
        )
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_contact = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'user_contact']

    objects = ProfileManager()

    def __str__(self):
        return self.user_name