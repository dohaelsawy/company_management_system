from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    num_departments = models.IntegerField(default=0)
    num_employees = models.IntegerField(default=0)
    num_projects = models.IntegerField(default=0)