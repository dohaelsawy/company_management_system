from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .models import Project, Company, Department, Employee

User = get_user_model()

class ProjectViewSetTests(TestCase):

    def setUp(self):
        
        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass', role='admin')
        self.manager_user = User.objects.create_user(username='manager', email='manager@example.com', password='managerpass', role='manager')
        self.employee_user = User.objects.create_user(username='employee', email='employee@example.com', password='employeepass', role='employee')
        
        self.company = Company.objects.create(name='Test Company', num_projects=0)
        self.department = Department.objects.create(name='Test Department', company=self.company, num_projects=0)

        self.admin_employee = Employee.objects.create(
            user=self.admin_user,
            name='Admin Employee',
            mobile='01111111111',
            address='Admin Address',
            title='Admin Title',
            company=self.company,
            department=self.department
        )
        self.manager_employee = Employee.objects.create(
            user=self.manager_user,
            name='Manager Employee',
            mobile='02222222222',
            address='Manager Address',
            title='Manager Title',
            company=self.company,
            department=self.department
        )
        self.employee_employee = Employee.objects.create(
            user=self.employee_user,
            name='Employee Employee',
            mobile='03333333333',
            address='Employee Address',
            title='Employee Title',
            company=self.company,
            department=self.department
        )

        
        self.project = Project.objects.create(
            name='Test Project',
            company=self.company,
            department=self.department,
            description='Test Description',
            start_date='2023-01-01T00:00:00Z',
            end_date='2023-12-31T00:00:00Z'
        )
        self.project.assigned_employees.add(self.employee_employee)

        self.client = Client()


    def test_retrieve_project_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('project-detail', args=[self.project.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.project.name)



    def test_retrieve_project_as_employee(self):
        self.client.force_login(self.employee_user)
        response = self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.project.name)


    def test_create_project_as_admin(self):
        
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse('project-list'),
            {
                'name': 'New Project',
                'company': self.company.id,
                'department': self.department.id,
                'description': 'New Description',
                'start_date': '2023-01-01T00:00:00Z',
                'end_date': '2023-12-31T00:00:00Z',
                'assigned_employees': [self.employee_employee.id]
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.company.refresh_from_db()
        self.department.refresh_from_db()
        self.assertEqual(self.company.num_projects, 2)
        self.assertEqual(self.department.num_projects, 2)

    def test_delete_project_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.delete(reverse('project-detail', args=[self.project.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)
        self.company.refresh_from_db()
        self.department.refresh_from_db()
        self.assertEqual(self.company.num_projects, 0)
        self.assertEqual(self.department.num_projects, 0)