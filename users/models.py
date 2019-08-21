from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, names=None, surname=None, password=None, is_staff=True, is_admin=True,
                    is_active=True, user_type="specialist"):
        if email is None:
            raise TypeError('Users must have an email address.')
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.names = names
        user_obj.surname = surname
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.user_type = user_type
        user_obj.save(using=self.db)
        token = Token.objects.create(user=user_obj)
        return user_obj

    def create_staffuser(self, email, password=None, names=None, surname=None):
        user = self.create_user(
            email,
            password=password,
            names=names,
            surname=surname,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, password=None, names=None, surname=None, user_type=None):
        user = self.create_user(
            email,
            password=password,
            names=names,
            surname=surname,
            is_staff=True,
            is_admin=True,
            user_type="administrator"
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ("administrator", "administrator"),
        ("specialist", "specialist")
    )
    names = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=70, unique=True)
    password = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    user_type = models.CharField(max_length=100,choices=USER_TYPES, default="administrator")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['names', 'surname', 'password', ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
