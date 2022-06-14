from unittest import mock

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from praktekiin.test import create_pengguna_and_login
from rekam_medis.models import Pasien
from rekam_medis.serializers import PasienSerializer


class PasienAPITestCase(APITestCase):
    url = '/rekam_medis/pasien/'

    def setUp(self):
        login_data = {'username': 'dimas', 'password': 'd'}
        self.pengguna = create_pengguna_and_login(self.client, login_data)

        Pasien.objects.create(
            nama='Dimas',
            nama_kk='Dimas',
            alamat='Depok',
            pekerjaan='Mahasiswa',
            tanggal_lahir='2000-01-01',
            jenis_kelamin='L',
            no_telp='0123456789012',
            dibuat_oleh=self.pengguna,
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
            'jenis_kelamin': 'P',
            'no_telp': '0123456789012',
        }

        now = timezone.now()
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=now)):
            response = self.client.post(self.url, data)

        data['id'] = 2
        data['dibuat_oleh'] = self.pengguna.id
        data['waktu_dibuat'] = now.isoformat()[:-6] + 'Z'

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
            'jenis_kelamin': 'L',
            'no_telp': '0123456789012',
        }

        waktu_dibuat = Pasien.objects.get(
            id=1).waktu_dibuat.isoformat()[:-6] + 'Z'

        response = self.client.put(self.url + '1/', data)
        data['id'] = 1
        data['dibuat_oleh'] = self.pengguna.id
        data['waktu_dibuat'] = waktu_dibuat

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_pasien_update_without_dibuat_oleh(self):
        pasien = Pasien.objects.create(
            nama='Tasya',
            nama_kk='Dimas',
            alamat='Depok',
            pekerjaan='Mahasiswa',
            tanggal_lahir='2000-02-01',
            jenis_kelamin='P',
            no_telp='0123456789012',
        )

        data = {
            'nama': 'Tasya',
            'nama_kk': 'Dimas',
            'alamat': 'Depok',
            'pekerjaan': 'PNS',
            'tanggal_lahir': '2000-02-01',
            'jenis_kelamin': 'P',
            'no_telp': '0123456787654',
        }

        waktu_dibuat = pasien.waktu_dibuat.isoformat()[:-6] + 'Z'
        response = self.client.put(self.url + str(pasien.id) + '/', data)
        data['id'] = pasien.id
        data['dibuat_oleh'] = self.pengguna.id
        data['waktu_dibuat'] = waktu_dibuat

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_pasien_destroy(self):
        response = self.client.delete(self.url + '1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pasien.objects.count(), 0)
