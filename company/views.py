from rest_framework import viewsets, status
from .models import Company
from .serializers import CompanySerializer
from utils.permissions import IsAdmin, IsManager, IsEmployee
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import Http404


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
        
            

    # def retrieve(self, request, pk=None):
    #     try:
    #         user = get_object_or_404(Company, pk=pk)
    #         serializer = CompanySerializer(user)
    #         return Response(serializer.data)
    #     except Http404:
    #         return Response(
    #             {'error': "The requested Company does not exist."}, 
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

