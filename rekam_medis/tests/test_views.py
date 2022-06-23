from unittest import mock

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from praktekiin.test import create_pengguna_and_login
from rekam_medis.models import Pasien
from rekam_medis.serializers import PasienSerializer

from pprint import pprint


class PasienAPITestCase(APITestCase):
    url = '/rekam_medis/pasien/'

    def setUp(self):
        login_data = {'username': 'dimas', 'password': 'd'}
        self.pengguna = create_pengguna_and_login(self.client, login_data)

        Pasien.objects.create(
            nama='Dimas',
            jenis_kelamin='L',
            nama_kk='Dimas',
            tempat_lahir='Depok',
            tanggal_lahir='2000-01-01',
            nama_ayah_suami='John Smith',
            alamat='Maharaja',
            alamat_rt='001',
            alamat_rw='002',
            alamat_kel_desa='Kel',
            alamat_kecamatan='Kec',
            alamat_kota_kab='Depok',
            alamat_provinsi='Jawa Barat',
            alamat_kode_pos='12345',
            no_telp='0123456789012',
            pekerjaan='Mahasiswa',
            status_perkawinan='BL',
            agama='islam',
            cara_bayar='C',
            tanggal='2022-06-01',
            promosi=True,
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
            'jenis_kelamin': 'P',
            'nama_kk': 'Dimas',
            'tempat_lahir': 'Depok',
            'tanggal_lahir': '2000-01-01',
            'nama_ayah_suami': 'John Smith',
            'alamat': 'Maharaja',
            'alamat_rt': '001',
            'alamat_rw': '002',
            'alamat_kel_desa': 'Kel',
            'alamat_kecamatan': 'Kec',
            'alamat_kota_kab': 'Depok',
            'alamat_provinsi': 'Jawa Barat',
            'alamat_kode_pos': '12345',
            'no_telp': '0123456789012',
            'pekerjaan': 'Mahasiswa',
            'status_perkawinan': '',
            'agama': 'islam',
            'cara_bayar': 'C',
            'tanggal': '2022-06-01',
            'promosi': False,
        }

        now = timezone.now()
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=now)):
            response = self.client.post(self.url, data)

        data['id'] = 2
        data['dibuat_oleh'] = self.pengguna.id
        data['waktu_dibuat'] = now.astimezone().isoformat()
        data['waktu_diubah'] = now.astimezone().isoformat()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        self.assertEqual(Pasien.objects.count(), 2)

    def test_pasien_create_only_with_required_fields(self):
        data = {
            'nama': 'Tasya',
            'jenis_kelamin': 'P',
            'nama_kk': 'Dimas',
            'tempat_lahir': '',
            'tanggal_lahir': '2000-01-01',
            'nama_ayah_suami': '',
            'alamat': 'Maharaja',
            'alamat_rt': '',
            'alamat_rw': '',
            'alamat_kel_desa': '',
            'alamat_kecamatan': '',
            'alamat_kota_kab': '',
            'alamat_provinsi': '',
            'alamat_kode_pos': '',
            'no_telp': '',
            'pekerjaan': 'Mahasiswa',
            'status_perkawinan': '',
            'agama': '',
            'cara_bayar': '',
            # 'tanggal': None,
            'promosi': False,
        }

        now = timezone.now()
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=now)):
            response = self.client.post(self.url, data)
        data['id'] = 2
        data['dibuat_oleh'] = self.pengguna.id
        data['waktu_dibuat'] = now.astimezone().isoformat()
        data['waktu_diubah'] = now.astimezone().isoformat()
        data['tanggal'] = None

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
            'jenis_kelamin': 'L',
            'nama_kk': 'Dimas',
            'tempat_lahir': 'Depok',
            'tanggal_lahir': '2000-01-01',
            'nama_ayah_suami': 'John Smith',
            'alamat': 'Maharaja',
            'alamat_rt': '001',
            'alamat_rw': '002',
            'alamat_kel_desa': 'Kel',
            'alamat_kecamatan': 'Kec',
            'alamat_kota_kab': 'Depok',
            'alamat_provinsi': 'Jawa Barat',
            'alamat_kode_pos': '12345',
            'no_telp': '0123456789012',
            'pekerjaan': 'PNS',
            'status_perkawinan': '',
            'agama': 'islam',
            'cara_bayar': 'C',
            'tanggal': '2022-06-01',
            'promosi': False,
        }

        pasien = Pasien.objects.get(id=1)
        waktu_dibuat = pasien.waktu_dibuat.astimezone().isoformat()

        now = timezone.now()
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=now)):
            response = self.client.put(self.url + '1/', data)

        data['id'] = 1
        data['dibuat_oleh'] = self.pengguna.id
        data['waktu_dibuat'] = waktu_dibuat
        data['waktu_diubah'] = now.astimezone().isoformat()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_pasien_update_without_dibuat_oleh_will_set(self):
        pasien = Pasien.objects.create(
            nama='Tasya',
            jenis_kelamin='P',
            nama_kk='Dimas',
            tempat_lahir='Depok',
            tanggal_lahir='2000-01-01',
            nama_ayah_suami='John Smith',
            alamat='Maharaja',
            alamat_rt='001',
            alamat_rw='002',
            alamat_kel_desa='Kel',
            alamat_kecamatan='Kec',
            alamat_kota_kab='Depok',
            alamat_provinsi='Jawa Barat',
            alamat_kode_pos='12345',
            no_telp='0123456789012',
            pekerjaan='Mahasiswa',
            status_perkawinan='BL',
            agama='islam',
            cara_bayar='C',
            tanggal='2022-06-01',
            promosi=True,
        )

        data = {
            'nama': 'Tasya',
            'jenis_kelamin': 'P',
            'nama_kk': 'Dimas',
            'tempat_lahir': 'Depok',
            'tanggal_lahir': '2000-01-01',
            'nama_ayah_suami': 'John Smith',
            'alamat': 'Maharaja',
            'alamat_rt': '001',
            'alamat_rw': '002',
            'alamat_kel_desa': 'Kel',
            'alamat_kecamatan': 'Kec',
            'alamat_kota_kab': 'Depok',
            'alamat_provinsi': 'Jawa Barat',
            'alamat_kode_pos': '12345',
            'no_telp': '0123456789012',
            'pekerjaan': 'PNS',
            'status_perkawinan': '',
            'agama': 'islam',
            'cara_bayar': 'C',
            'tanggal': '2022-06-01',
            'promosi': False,
        }

        waktu_dibuat = pasien.waktu_dibuat.astimezone().isoformat()

        now = timezone.now()
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=now)):
            response = self.client.put(self.url + str(pasien.id) + '/', data)

        data['id'] = pasien.id
        data['dibuat_oleh'] = self.pengguna.id
        data['waktu_dibuat'] = waktu_dibuat
        data['waktu_diubah'] = now.astimezone().isoformat()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_pasien_destroy(self):
        response = self.client.delete(self.url + '1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pasien.objects.count(), 0)
