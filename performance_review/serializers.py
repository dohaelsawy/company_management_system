from rest_framework import serializers
from .models import PerformanceReview

class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = ['id', 'employee', 'stage', 'review_date', 'feedback', 'created_at', 'updated_at']