from rest_framework import viewsets, status
from .models import Department
from .serializers import DepartmentSerializer
from utils.permissions import IsAdmin, IsManager, IsEmployee
from rest_framework.response import Response
from rest_framework import serializers



class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []

    def get_permissions(self):

        if self.action in ["retrieve", "list"]:
            self.permission_classes = [IsAdmin | IsManager | IsEmployee]
        else :
            self.permission_classes = [IsAdmin]

        return super().get_permissions()
    


        

