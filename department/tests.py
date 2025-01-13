from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .models import Department, Company

User = get_user_model()

class DepartmentViewSetTests(TestCase):
    def setUp(self):

        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', role='admin')
        
        self.manager_user = User.objects.create_user(username='manager', email='manager@example.com', role='manager')
        
        self.employee_user = User.objects.create_user(username='employee', email='employee@example.com',role='employee')
        
        self.company = Company.objects.create(name='Test Company', num_departments=0)
        self.department = Department.objects.create(name='Test Department', company=self.company)

        self.client = Client()

    def test_retrieve_department_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('department-detail', args=[self.department.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.department.name)



    def test_retrieve_department_as_manager(self):

        self.client.force_login(self.manager_user)
        response = self.client.get(reverse('department-detail', args=[self.department.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.department.name)



    def test_retrieve_department_as_employee(self):

        self.client.force_login(self.employee_user)
        response = self.client.get(reverse('department-detail', args=[self.department.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.department.name)



    def test_create_department_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('department-list'),
            {'name': 'New Department', 'company': self.company.id},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)
        self.company.refresh_from_db()
        self.assertEqual(self.company.num_departments, 2)



    def test_create_department_as_manager(self):

        self.client.force_login(self.manager_user)
        response = self.client.post(
            reverse('department-list'),
            {'name': 'New Department', 'company': self.company.id},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_create_department_as_employee(self):

        self.client.force_login(self.employee_user)
        response = self.client.post(
            reverse('department-list'),
            {'name': 'New Department', 'company': self.company.id},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_update_department_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.put(
            reverse('department-detail', args=[self.department.id]),
            {'name': 'Updated Department', 'company': self.company.id},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, 'Updated Department')



    def test_delete_department_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.delete(reverse('department-detail', args=[self.department.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)
        self.company.refresh_from_db()
        self.assertEqual(self.company.num_departments, 0)

    def test_retrieve_nonexistent_department(self):

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('department-detail', args=[999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)