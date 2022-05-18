from rest_framework import status

from tests.test_setup import TestSetUp


class LoginTestCase(TestSetUp):
    """
    Clase para realizar testing sobre el login con token
    """

    def test_fail_auth(self):
        """
        Metodo para controlar una autenticación fallida
        """
        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password': 'fail'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
