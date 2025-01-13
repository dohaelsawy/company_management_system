from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer
from utils.permissions import IsAdmin, IsManager, IsEmployee


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
    


        

