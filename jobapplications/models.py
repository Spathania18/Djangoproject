from django.db import models
import datetime

# Create your models here.
class applications(models.Model):
    username = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    applied_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.username} - {self.job_title}"