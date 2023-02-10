from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from akun.models import Pengguna


class AkunAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'dimas',
            'password': 'asdf1234',
            'nama_panggilan': 'Dimas',
            'no_hp': '081122334455',
            'peran': Pengguna.Role.STAF_ADMIN
        }
        Pengguna.objects.create_user(**self.user_data)

    def test_masuk(self):
        response = self.client.post('/akun/masuk/', self.user_data)

        token = Token.objects.get(user__username=self.user_data['username'])
        self.assertEqual(response.data, {
            'token': token.key,
            'pengguna': {
                'id': 1,
                'username': 'dimas',
                'nama_panggilan': 'Dimas',
                'no_hp': '081122334455',
                'peran': 'ADM',
                'peran_nama': 'Staf Administrasi',
            }
        })

    def test_keluar(self):
        token = self.client.post('/akun/masuk/', self.user_data).data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post('/akun/keluar/')
        tokens = Token.objects.filter(
            user__username=self.user_data['username'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'Berhasil keluar.'})
        self.assertEqual(tokens.count(), 0)
