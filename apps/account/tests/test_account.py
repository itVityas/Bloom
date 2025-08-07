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
        self.admin = User.objects.create_superuser(
            username='testadmin',
            password='ASDqwe12#'
        )
        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', args=[self.user.id])

    def test_user_list(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
