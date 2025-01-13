from django.db import models
from employee.models import Employee
from django.core.exceptions import ValidationError


class PerformanceReview(models.Model):
    STAGE_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('review_scheduled', 'Review Scheduled'),
        ('feedback_provided', 'Feedback Provided'),
        ('under_approval', 'Under Approval'),
        ('review_approved', 'Review Approved'),
        ('review_rejected', 'Review Rejected'),
    ]

    ALLOWED_TRANSITIONS = {
        'pending_review': ['review_scheduled'],
        'review_scheduled': ['feedback_provided'],
        'feedback_provided': ['under_approval'],
        'under_approval': ['review_approved', 'review_rejected'],
        'review_rejected': ['feedback_provided'],
        'review_approved': [],
    }

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='employee_performance_reviews', 
        related_query_name='employee_performance_review'
    )    
    
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='pending_review')
    review_date = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Performance Review for {self.employee.name} ({self.get_stage_display()})"
    
    
    def transition_to(self, new_stage):

        if new_stage not in dict(self.STAGE_CHOICES):
            raise ValidationError(f"Invalid stage: {new_stage}")

        allowed_transitions = self.ALLOWED_TRANSITIONS.get(self.stage, [])
        if new_stage not in allowed_transitions:
            raise ValidationError(f"Cannot transition from {self.stage} to {new_stage}")

        self.stage = new_stage
        self.save()

    
    
    def schedule_review(self, review_date):
        if self.stage != 'pending_review':
            raise ValueError("Cannot schedule review unless the stage is 'Pending Review'.")
        self.stage = 'review_scheduled'
        self.review_date = review_date
        self.save()

    def provide_feedback(self, feedback):
        if self.stage != 'review_scheduled':
            raise ValueError("Cannot provide feedback unless the stage is 'Review Scheduled'.")
        self.stage = 'feedback_provided'
        self.feedback = feedback
        self.save()

    def submit_for_approval(self):
        if self.stage != 'feedback_provided':
            raise ValueError("Cannot submit for approval unless the stage is 'Feedback Provided'.")
        self.stage = 'under_approval'
        self.save()

    def approve_review(self):
        if self.stage != 'under_approval':
            raise ValueError("Cannot approve review unless the stage is 'Under Approval'.")
        self.stage = 'review_approved'
        self.save()

    def reject_review(self):
        if self.stage != 'under_approval':
            raise ValueError("Cannot reject review unless the stage is 'Under Approval'.")
        self.stage = 'review_rejected'
        self.save()

    def update_feedback(self, feedback):
        if self.stage != 'review_rejected':
            raise ValueError("Cannot update feedback unless the stage is 'Review Rejected'.")
        self.stage = 'feedback_provided'
        self.feedback = feedback
        self.save()