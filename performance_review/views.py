# views.py (updated)
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer
from utils.permissions import IsAdmin, IsManager


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = []

    def get_permissions(self):

        if self.action in ["retrieve", "list"]:
            self.permission_classes = [IsAdmin | IsManager]
        else :
            self.permission_classes = [IsAdmin]

        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def schedule_review(self, request, pk=None):
        review = self.get_object()
        review_date = request.data.get('review_date')
        try:
            review.schedule_review(review_date)
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def provide_feedback(self, request, pk=None):
        review = self.get_object()
        feedback = request.data.get('feedback')
        try:
            review.provide_feedback(feedback)
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def submit_for_approval(self, request, pk=None):
        review = self.get_object()
        try:
            review.submit_for_approval()
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def approve_review(self, request, pk=None):
        review = self.get_object()
        try:
            review.approve_review()
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject_review(self, request, pk=None):
        review = self.get_object()
        try:
            review.reject_review()
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_feedback(self, request, pk=None):
        review = self.get_object()
        feedback = request.data.get('feedback')
        try:
            review.update_feedback(feedback)
            serializer = self.get_serializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)