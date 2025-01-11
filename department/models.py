from django.db import models
from company.models import Company

class Department(models.Model):
    name = models.CharField(max_length=200)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    num_employees = models.IntegerField(default=0)
    num_projects = models.IntegerField(default=0)