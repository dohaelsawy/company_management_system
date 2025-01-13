from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .models import Employee, Company, Department
from django.utils import timezone


User = get_user_model()

class EmployeeViewSetTests(TestCase):

    def setUp(self):

        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', role='admin')
        
        self.manager_user = User.objects.create_user(username='manager', email='manager@example.com', role='manager')
        
        self.employee_user = User.objects.create_user(username='employee', email='employee@example.com', role='employee')
        
        self.company = Company.objects.create(name='Test Company', num_employees=0)
        
        self.department = Department.objects.create(name='Test Department', company=self.company, num_employees=0)
        
        self.employee = Employee.objects.create(
            name='Test Employee',
            company=self.company,
            department=self.department,
            user=self.employee_user,
            mobile='01111111111',
            address='Test Address',
            title='Test Title'
        )

        self.client = Client()

    def test_retrieve_employee_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('employee-detail', args=[self.employee.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee.name)



    def test_retrieve_employee_as_employee(self):

        self.client.force_login(self.employee_user)
        response = self.client.get(reverse('employee-detail', args=[self.employee.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee.name)



    def test_create_employee_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('employee-list'),
            {'name': 'New Employee', 'company': self.company.id, 'department': self.department.id, 'user': self.employee_user.id, 'mobile': '02222222222', 'address': 'New Address', 'title': 'New Title'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.company.refresh_from_db()
        self.department.refresh_from_db()
        self.assertEqual(self.company.num_employees, 1)
        self.assertEqual(self.department.num_employees, 1)



    def test_delete_employee_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.delete(reverse('employee-detail', args=[self.employee.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
        self.company.refresh_from_db()
        self.department.refresh_from_db()
        self.assertEqual(self.company.num_employees, 0)
        self.assertEqual(self.department.num_employees, 0)



    def test_retrieve_employee_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('employee-detail', args=[self.employee.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee.name)



    def test_create_employee_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('employee-list'),
            {'name': 'New Employee', 'company': self.company.id, 'department': self.department.id, 'user': self.admin_user.id, 'mobile': '02222222222', 'address': 'New Address', 'title': 'New Title', 'hired_on': timezone.now()},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.company.refresh_from_db()
        self.department.refresh_from_db()
        self.assertEqual(self.company.num_employees, 2)
        self.assertEqual(self.department.num_employees, 2)



    def test_delete_employee_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.delete(reverse('employee-detail', args=[self.employee.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
        self.company.refresh_from_db()
        self.department.refresh_from_db()
        self.assertEqual(self.company.num_employees, 0)
        self.assertEqual(self.department.num_employees, 0)
