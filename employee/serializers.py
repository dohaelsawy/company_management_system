from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'mobile', 'address', 'title', 'hired_on', 'days_hired', 'company', 'department', 'user']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            request = self.context.get('request', None)

            if request and request.user.role == 'employee':
                self.Meta.read_only_fields = ['title', 'hired_on', 'days_hired', 'company', 'department', 'user']
            
            else:       
                self.Meta.read_only_fields = []

    def validate_mobile(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("Mobile number must be exactly 11 characters.")
        return value