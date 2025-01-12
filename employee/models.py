from django.db import models
from company.models import Company
from department.models import Department
from user.models import User
from django.utils.timezone import now

class Employee(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    hired_on = models.DateTimeField(null=True)
    @property
    def days_hired(self):
        if self.hired_on:
            return (now().date() - self.hired_on).days
        return None

