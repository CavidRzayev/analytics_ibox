from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import datetime,timedelta
from django.conf import settings
from django.core import validators



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=True, is_manager=True):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        

        user_obj = self.model(
        email=self.normalize_email(email),
        
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.is_manager = is_manager
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password):
        user = self.create_user(
        email,
        password=password,
        is_staff=True,
        is_admin=True,
        is_manager=True
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=25, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    objects = UserManager()
    USERNAME_FIELD = 'email'


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def set_unusable_password(self):
        return True

    