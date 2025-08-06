import json

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from apps.account.models import User


class UserCRUDTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
