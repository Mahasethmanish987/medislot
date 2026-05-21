from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(
            self, 
            email: str, 
            username: str, 
            first_name: str, 
            last_name: str, 
            phone_number: str, 
            password: str = None
            ) -> 'User':
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.is_active = True
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(
            self,
            email: str,
            username: str,
            first_name: str,
            last_name: str,
            phone_number: str,
            password: str = None
    ) -> 'User':
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user 

class User(AbstractBaseUser, PermissionsMixin):
    DOCTOR= 1
    PATIENT = 2
    CHOICES = ((DOCTOR, "Doctor"), (PATIENT, "Patient"))

    email = models.EmailField(unique=True,max_length=255)
    username = models.CharField(max_length=255,unique=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    role = models.PositiveSmallIntegerField(choices=CHOICES,blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number"]
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_role(self):
        return self.role
    
