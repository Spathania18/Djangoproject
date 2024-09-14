from django.contrib import admin
from jobapplications.models import applications
# Register your models here.

class applicationsadmin(admin.ModelAdmin):
    list_display = ('username', 'company_name', 'job_title', 'job_type', 'applied_date')


admin.site.register(applications, applicationsadmin)