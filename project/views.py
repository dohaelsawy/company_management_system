from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from utils.permissions import IsAdmin, IsManager, IsEmployee

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action in ["retrieve"]:
            self.permission_classes = [IsAdmin | IsManager | IsEmployee]
        else:
            self.permission_classes = [IsAdmin | IsManager]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'employee':
            return Project.objects.filter(assigned_employees__user=user)
        return Project.objects.all()