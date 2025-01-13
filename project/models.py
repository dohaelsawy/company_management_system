from django.db import models
from company.models import Company
from department.models import Department
from employee.models import Employee


class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigned_employees = models.ManyToManyField(Employee)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.company.num_projects += 1
            self.company.save()

            self.department.num_projects += 1
            self.department.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.company.num_projects -= 1
        self.company.save()

        self.department.num_projects -= 1
        self.department.save()
        super().delete(*args, **kwargs)


