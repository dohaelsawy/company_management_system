from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer
from utils.permissions import IsAdmin, IsManager, IsEmployee

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []

    def get_permissions(self):

        if self.action in ["retrieve", "list"]:
            self.permission_classes = [IsAdmin | IsManager | IsEmployee]
        else :
            self.permission_classes = [IsAdmin]

        return super().get_permissions()
        

