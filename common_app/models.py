import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import MyAccountManager

def generate_random_string():
    random_uuid = uuid.uuid4()
    return random_uuid.hex

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Email should be unique and required for authentication
    full_name = models.CharField(max_length=255, blank=True)  # Optional field for additional user information
    contact = models.CharField(max_length=10, blank=True, unique=True)  # Optional contact number

    is_active = models.BooleanField(default=True)  # Indicates if the user account is active
    is_staff = models.BooleanField(default=False)  # Indicates if the user has access to admin interface
    is_superuser = models.BooleanField(default=False)  # Indicates if the user has superuser privileges

    USERNAME_FIELD = 'email'  # The field to use for authentication
    REQUIRED_FIELDS = []  # Fields that are required for creating a user through the command line

    objects = MyAccountManager()  # Custom user manager

    def __str__(self):
        return self.email

    @property
    def full_contact_number(self):
        return f'+91 - {self.contact}' if self.contact else 'No contact present'
