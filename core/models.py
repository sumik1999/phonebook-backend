from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, *args, **kwargs):
        if not phone_number:
            raise ValueError("Users must have phone number")
        user = self.model(phone_number=phone_number, *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=512, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=10, unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "phone_number"


class GlobalContact(models.Model):
    phone_number = models.CharField(max_length=10, blank=False, null=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=512, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="owner")
    is_spam = models.BooleanField(default=False)
