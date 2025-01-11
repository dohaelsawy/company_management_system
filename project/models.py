from django.db import models
from company.models import Company
from department.models import Department
from employee.models import Employee


class Project(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigned_employees = models.ManyToManyField(Employee)
