from django.db import models
from company.models import Company
from department.models import Department
from user.models import User
from django.utils.timezone import now

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    hired_on = models.DateTimeField(null=True)
    @property
    def days_hired(self):
        if self.hired_on:
            return (now() - self.hired_on).days
        return None
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.company.num_departments += 1
            self.company.save()

            self.department.num_employees += 1
            self.department.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.company.num_departments -= 1
        self.company.save()

        self.department.num_employees -= 1
        self.department.save()
        super().delete(*args, **kwargs)

