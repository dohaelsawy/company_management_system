from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from employee.models import Employee
from .models import PerformanceReview
from django.contrib.auth import get_user_model
from company.models import Company
from department.models import Department


User = get_user_model()

class PerformanceReviewViewSetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='manager', email='manager@example.com', role='manager')
        
        self.company = Company.objects.create(name='Test Company', num_employees=0)
        self.department = Department.objects.create(name='Test Department', company=self.company, num_employees=0)

        self.employee = Employee.objects.create(
            name='Test Employee',
            company=self.company,
            department=self.department,
            user=self.user,
            mobile='01111111111',
            address='Test Address',
            title='Test Title'
        )

        self.review = PerformanceReview.objects.create(
            employee=self.employee,
            stage='pending_review'
        )

        self.client = Client()
        self.client.force_login(self.user)



    def test_schedule_review_valid(self):

        url = reverse('performancereview-schedule-review', args=[self.review.id])
        response = self.client.post(url, {'review_date': '2023-10-15T10:00:00Z'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.stage, 'review_scheduled')
        self.assertEqual(str(self.review.review_date), '2023-10-15 10:00:00+00:00')



    def test_schedule_review_invalid(self):

        self.review.stage = 'feedback_provided'
        self.review.save()
        url = reverse('performancereview-schedule-review', args=[self.review.id])
        response = self.client.post(url, {'review_date': '2023-10-15T10:00:00Z'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Cannot schedule review unless the stage is 'Pending Review'.")



    def test_provide_feedback_valid(self):

        self.review.stage = 'review_scheduled'
        self.review.save()
        url = reverse('performancereview-provide-feedback', args=[self.review.id])
        response = self.client.post(url, {'feedback': 'Good performance.'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.stage, 'feedback_provided')
        self.assertEqual(self.review.feedback, 'Good performance.')



    def test_provide_feedback_invalid(self):
        url = reverse('performancereview-provide-feedback', args=[self.review.id])
        response = self.client.post(url, {'feedback': 'Good performance.'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Cannot provide feedback unless the stage is 'Review Scheduled'.")



    def test_submit_for_approval_valid(self):

        self.review.stage = 'feedback_provided'
        self.review.save()
        url = reverse('performancereview-submit-for-approval', args=[self.review.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.stage, 'under_approval')



    def test_submit_for_approval_invalid(self):

        url = reverse('performancereview-submit-for-approval', args=[self.review.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Cannot submit for approval unless the stage is 'Feedback Provided'.")



    def test_approve_review_valid(self):

        self.review.stage = 'under_approval'
        self.review.save()
        url = reverse('performancereview-approve-review', args=[self.review.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.stage, 'review_approved')



    def test_approve_review_invalid(self):

        url = reverse('performancereview-approve-review', args=[self.review.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Cannot approve review unless the stage is 'Under Approval'.")

    def test_reject_review_valid(self):

        self.review.stage = 'under_approval'
        self.review.save()
        url = reverse('performancereview-reject-review', args=[self.review.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.stage, 'review_rejected')



    def test_reject_review_invalid(self):

        url = reverse('performancereview-reject-review', args=[self.review.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Cannot reject review unless the stage is 'Under Approval'.")



    def test_update_feedback_valid(self):

        self.review.stage = 'review_rejected'
        self.review.save()
        url = reverse('performancereview-update-feedback', args=[self.review.id])
        response = self.client.post(url, {'feedback': 'Updated feedback.'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.stage, 'feedback_provided')
        self.assertEqual(self.review.feedback, 'Updated feedback.')



    def test_update_feedback_invalid(self):
        url = reverse('performancereview-update-feedback', args=[self.review.id])
        response = self.client.post(url, {'feedback': 'Updated feedback.'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Cannot update feedback unless the stage is 'Review Rejected'.")