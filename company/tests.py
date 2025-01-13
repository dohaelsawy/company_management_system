from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .models import Company

User = get_user_model()

class CompanyViewSetTests(TestCase):
   
    def setUp(self):
        
        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass', role='admin')

        self.manager_user = User.objects.create_user(username='manager', email='manager@example.com', password='managerpass', role='manager')
        
        self.employee_user = User.objects.create_user(username='employee', email='employee@example.com', password='employeepass', role='employee')
        
        self.company = Company.objects.create(name='Test Company')

        self.client = Client()



    def test_retrieve_company_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('company-detail', args=[self.company.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.company.name)



    def test_retrieve_company_as_manager(self):
        
        self.client.force_login(self.manager_user)
        response = self.client.get(reverse('company-detail', args=[self.company.id]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.company.name)



    def test_retrieve_company_as_employee(self):

        self.client.force_login(self.employee_user)
        response = self.client.get(reverse('company-detail', args=[self.company.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.company.name)



    def test_create_company_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('company-list'), {'name': 'New Company'}, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)



    def test_create_company_as_manager(self):

        self.client.force_login(self.manager_user)
        response = self.client.post(reverse('company-list'), {'name': 'New Company'}, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_create_company_as_employee(self):

        self.client.force_login(self.employee_user)
        response = self.client.post(reverse('company-list'), {'name': 'New Company'}, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_update_company_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.put(
            reverse('company-detail', args=[self.company.id]),
            {'name': 'Updated Company'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'Updated Company')



    def test_delete_company_as_admin(self):

        self.client.force_login(self.admin_user)
        response = self.client.delete(reverse('company-detail', args=[self.company.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)



    def test_retrieve_nonexistent_company(self):

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('company-detail', args=[999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)