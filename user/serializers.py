from rest_framework import serializers
from .models import User

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
