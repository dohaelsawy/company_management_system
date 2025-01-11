from django.db import models

role_choice = {
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('employee', 'Employee'),
}

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    role = models.CharField(choices = role_choice)
