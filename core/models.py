from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


# For creating a custom user model and model manager
class UserManager(BaseUserManager):
    """user manager for the custom user model"""
    def create_user(self, email, password=None, **kwargs):
        """create and save a new user"""
        if not email:
            raise ValueError('Users must have a valid email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """create and save a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
