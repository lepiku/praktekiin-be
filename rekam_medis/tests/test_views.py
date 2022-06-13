from rest_framework import status
from rest_framework.test import APITestCase

from akun.models import Pengguna
from rekam_medis.models import Pasien
from rekam_medis.serializers import PasienSerializer


class PasienTest(APITestCase):
    url = '/rekam_medis/pasien/'

    def setUp(self):
        login_data = {'username': 'dimas', 'password': 'd'}
        Pengguna.objects.create_user(**login_data)
        self.client.login(**login_data)

        Pasien.objects.create(
            nama='Dimas',
            nama_kk='Dimas',
            alamat='Depok',
            pekerjaan='Mahasiswa',
            tanggal_lahir='2000-01-01',
            no_telp='0123456789012',
        )

    def test_pasien_list(self):
        response = self.client.get(self.url)
        serializer = PasienSerializer(Pasien.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_pasien_create(self):
        data = {
            'nama': 'Tasya',
            'nama_kk': 'Dimas',
            'alamat': 'Depok',
            'pekerjaan': 'Mahasiswa',
            'tanggal_lahir': '2000-01-01',
            'no_telp': '0123456789012',
        }

        response = self.client.post(self.url, data)
        serializer = PasienSerializer(Pasien.objects.all(), many=True)
        data['id'] = 2

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        self.assertEqual(Pasien.objects.count(), 2)

    def test_pasien_retrieve(self):
        response = self.client.get(self.url + '1/')
        serializer = PasienSerializer(Pasien.objects.get(id=1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_pasien_update(self):
        data = {
            'nama': 'Dimas',
            'nama_kk': 'Dimas',
            'alamat': 'Depok',
            'pekerjaan': 'PNS',
            'tanggal_lahir': '2000-01-01',
            'no_telp': '0123456789012',
        }
        response = self.client.put(self.url + '1/', data)
        data['id'] = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_pasien_destroy(self):
        response = self.client.delete(self.url + '1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pasien.objects.count(), 0)
