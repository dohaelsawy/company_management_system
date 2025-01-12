from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer
from utils.permissions import IsAdmin, IsManager, IsEmployee

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAdmin | IsManager | IsEmployee]
        else:
            self.permission_classes = [IsAdmin | IsManager]
        return super().get_permissions()

#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'employee':
#             return Employee.objects.filter(user=user)
#         return Employee.objects.all()

#     def get_object(self):
#         obj = super().get_object()
#         user = self.request.user
#         if user.role == 'employee' and obj.user != user:
#             return Response({"detail": "You do not have permission to access this record."}, status=status.HTTP_403_FORBIDDEN)
#         return obj