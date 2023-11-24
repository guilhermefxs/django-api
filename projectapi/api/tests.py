from ast import literal_eval
import json
import io
import os
from urllib.parse import urlencode
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
from django.core.files import File
from django.template.loader import render_to_string
from .test_utils import all_teams, not_on_serie_a, order_by_data_and_page_size_2, page_size_and_page_number, search_sao_paulo

class CreateProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_profile_success_login_and_logout(self):
        data = {
            'name': 'Guilherme',
            'email': 'gui@example.com',
            'profileImage': File(open('test_image/link.png', 'rb')),
            'username': 'gui',
            'password': 'password123'
        }

        create_user_response = self.client.post('/api/profile-create/', data, format='multipart')

        self.assertEqual(create_user_response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Profile.objects.count(), 1)
        profile = Profile.objects.get()
        self.assertEqual(profile.name, 'Guilherme')
        self.assertEqual(profile.email, 'gui@example.com')

        login_data = {
            'username': 'gui',
            'password': 'password123'
        }

        login_response = self.client.post('/api/login/', login_data, format='multipart')

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        authToken = literal_eval(login_response.content.decode('utf-8'))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + authToken['token'])

        logout_response = self.client.post('/api/logout/')

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        os.remove('media_root/link.png')
        

    def test_create_profile_invalid_data(self):
        invalid_data = {'name': '', 'email': 'invalid_email', 'profileImage': 'invalid_image'}

        response = self.client.post('/api/profile-create/', invalid_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_agreement_endpoint(self):
        response = self.client.get('/api/get-user-agreement/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("Content-Type"), "application/pdf")

    def test_team_list(self):
        create_teams = self.client.post('/api/team-create/', json.loads(all_teams), format='json')
        self.assertEqual(create_teams.status_code, status.HTTP_201_CREATED)

        data = {
            'name': 'Guilherme',
            'email': 'gui@example.com',
            'profileImage': File(open('test_image/link.png', 'rb')),
            'username': 'gui',
            'password': 'password123'
        }

        create_user_response = self.client.post('/api/profile-create/', data, format='multipart')
        user = Profile.objects.get(username='gui')
        self.client.force_authenticate(user=user)

        orderBy = self.client.get('/api/teams-list/?orderBy=data_fundacao&page_size=2')
        self.assertEqual(orderBy.content.decode('utf-8'), order_by_data_and_page_size_2)

        search = self.client.get('/api/teams-list/?search=s%C3%A3o%20paulo')
        self.assertEqual(search.content.decode('utf-8'), search_sao_paulo)

        pageSize = self.client.get('/api/teams-list/?page_size=6&page=2')
        self.assertEqual(pageSize.content.decode('utf-8'), page_size_and_page_number)

        filter = self.client.get('/api/teams-list/?isOnSerieA=False')
        self.assertEqual(filter.content.decode('utf-8'), not_on_serie_a)
        os.remove('media_root/link.png')

        