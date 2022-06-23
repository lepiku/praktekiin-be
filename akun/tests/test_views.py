from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from akun.models import Pengguna


class AkunAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {'username': 'dimas', 'password': 'd',
                          'email': 'dimas@g.c', 'role': Pengguna.Role.ADMIN}
        Pengguna.objects.create_user(**self.user_data)

    def test_login(self):
        response = self.client.post('/akun/login/', self.user_data)

        token = Token.objects.get(user__username=self.user_data['username'])
        self.assertEqual(response.data, {
            'token': token.key,
            'pengguna': {
                'id': 1,
                'username': 'dimas',
                'email': 'dimas@g.c',
                'role': 'AD',
                'role_name': 'Admin',
            }
        })

    def test_logout(self):
        token = self.client.post('/akun/login/', self.user_data).data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post('/akun/logout/')
        tokens = Token.objects.filter(
            user__username=self.user_data['username'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'Logout success'})
        self.assertEqual(tokens.count(), 0)
