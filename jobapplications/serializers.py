from rest_framework import serializers
from .models import applications

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = applications
        fields = ['job_type', 'company_name', 'applied_date']
