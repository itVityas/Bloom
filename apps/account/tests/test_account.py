from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from apps.account.models import User


class UserCRUDTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='ASDqwe12#'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='SDFwer23$'
        )
        self.admin = User.objects.create_superuser(
            username='testadmin',
            password='ASDqwe12#'
        )
        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', args=[self.user.id])
        self.create_url = reverse('register')
        self.change_password_url = reverse('change_user_password')

    def test_user_list(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'username': 'XXXXXXX',
            'password': 'ASDqwe12#',
            'password2': 'ASDqwe12#',
            'fio': 'New User',
            'departmant': 'IT',
            'position': 'Developer',
            'room': '101'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_password(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'id': self.user2.id,
            'password': 'ASDqwe12#',
            'password2': 'ASDqwe12#'
        }
        response = self.client.patch(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
