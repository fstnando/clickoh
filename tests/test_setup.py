from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password


class TestSetUp(APITestCase):
    """
    Clase Generica que inicializa demas clases de testing
    """

    def setUp(self):
        """
        Configuración inicial donde se crea el usuario y se obtiene el token.
        """
        from django.contrib.auth.models import User

        faker = Faker()

        self.login_url = '/api/token/'
        self.user = User.objects.create_superuser(
            first_name=faker.name(),
            last_name=faker.name(),
            username=faker.name(),
            password='testing',
            email=faker.email()
        )

        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password': 'testing'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        return super().setUp()
