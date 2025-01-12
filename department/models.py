from django.db import models
from company.models import Company

class Department(models.Model):
    name = models.CharField(max_length=200)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    num_employees = models.IntegerField(default=0)
    num_projects = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.company_id.num_departments += 1
            self.company_id.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.company_id.num_departments -= 1
        self.company_id.save()
        super().delete(*args, **kwargs)