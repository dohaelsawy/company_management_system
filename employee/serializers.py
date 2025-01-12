from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'mobile', 'address', 'title', 'hired_on', 'days_hired', 'company_id', 'department_id', 'user_id']
        read_only_fields = ['title', 'hired_on', 'days_employed', 'company_id', 'department_id', 'user_id'] 

    def validate_mobile(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("Mobile number must be exactly 11 characters.")
        return value