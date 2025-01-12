from django.db import models
from django.contrib.auth.models import AbstractUser

role_choice = {
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('employee', 'Employee'),
}

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(choices = role_choice, default='employee')
    
