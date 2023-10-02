import pprint
from unittest import mock

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from akun.models import Pengguna
from praktekiin.test import create_pengguna_and_masuk
from rekam_medis.models import Pasien, Perjanjian
from rekam_medis.serializers import PasienSerializer


class PasienAPITestCase(APITestCase):
    url = "/rekam-medis/pasien/"

    def setUp(self):
        pengguna_data = {
            "username": "dimas",
            "password": "asdf1234",
            "nama_panggilan": "Dimas",
            "no_hp": "081122334450",
            "peran": Pengguna.Peran.STAF_ADMINISTRASI,
        }
        self.pengguna = create_pengguna_and_masuk(self.client, pengguna_data)

        pasien = Pasien.objects.create(
            nama="Dimas",
            jenis_kelamin="l",
            nama_kk="Dimas",
            tempat_lahir="Depok",
            tanggal_lahir="2000-01-01",
            alamat="Maharaja",
            alamat_rt="001",
            alamat_rw="002",
            alamat_kel_desa="Kel",
            alamat_kecamatan="Kec",
            alamat_kota_kab="Depok",
            alamat_provinsi="Jawa Barat",
            alamat_kode_pos="12345",
            no_hp="0123456789012",
            pekerjaan="Mahasiswa",
            status_perkawinan="belum_menikah",
            agama="islam",
            dibuat_oleh=self.pengguna,
        )
        pasien.dikelola_oleh.add(self.pengguna)

    def test_pasien_list(self):
        response = self.client.get(self.url)
        serializer = PasienSerializer(Pasien.objects.all().order_by("-id"), many=True)

        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": serializer.data,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_pasien_create(self):
        data = {
            "nama": "Tasya",
            "jenis_kelamin": "p",
            "nama_kk": "Dimas",
            "tempat_lahir": "Depok",
            "tanggal_lahir": "2000-01-01",
            "alamat": "Maharaja",
            "alamat_rt": "001",
            "alamat_rw": "002",
            "alamat_kel_desa": "Kel",
            "alamat_kecamatan": "Kec",
            "alamat_kota_kab": "Depok",
            "alamat_provinsi": "Jawa Barat",
            "alamat_kode_pos": "12345",
            "no_hp": "0123456789012",
            "pekerjaan": "Mahasiswa",
            "status_perkawinan": "",
            "agama": "islam",
        }

        now = timezone.now()
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=now)):
            response = self.client.post(self.url, data)

        data["id"] = 2
        data["dikelola_oleh"] = [self.pengguna.id]
        data["dibuat_oleh"] = self.pengguna.id
        data["waktu_dibuat"] = now.astimezone().isoformat()
        data["diubah_oleh"] = self.pengguna.id
        data["waktu_diubah"] = now.astimezone().isoformat()
        data["diarsipkan"] = False

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        self.assertEqual(Pasien.objects.count(), 2)

    def test_pasien_create_only_with_required_fields(self):
        data = {
            "nama": "Tasya",
            "jenis_kelamin": "p",
            "nama_kk": "",
            "tempat_lahir": "",
            "tanggal_lahir": "2000-01-01",
            "alamat": "Maharaja",
            "alamat_rt": "",
            "alamat_rw": "",
            "alamat_kel_desa": "",
            "alamat_kecamatan": "",
            "alamat_kota_kab": "",
            "alamat_provinsi": "",
            "alamat_kode_pos": "",
            "no_hp": "",
            "pekerjaan": "",
            "status_perkawinan": "",
            "agama": "",
        }

        now = timezone.now()
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=now)):
            response = self.client.post(self.url, data)
        data["id"] = 2
        data["dikelola_oleh"] = [self.pengguna.id]
        data["dibuat_oleh"] = self.pengguna.id
        data["waktu_dibuat"] = now.astimezone().isoformat()
        data["diubah_oleh"] = self.pengguna.id
        data["waktu_diubah"] = now.astimezone().isoformat()
        data["diarsipkan"] = False

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        self.assertEqual(Pasien.objects.count(), 2)

    def test_pasien_retrieve(self):
        response = self.client.get(self.url + "1/")
        serializer = PasienSerializer(Pasien.objects.get(id=1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_pasien_update(self):
        data = {
            "nama": "Dimas",
            "jenis_kelamin": "l",
            "nama_kk": "Dimas",
            "tempat_lahir": "Depok",
            "tanggal_lahir": "2000-01-01",
            "alamat": "Maharaja",
            "alamat_rt": "001",
            "alamat_rw": "002",
            "alamat_kel_desa": "Kel",
            "alamat_kecamatan": "Kec",
            "alamat_kota_kab": "Depok",
            "alamat_provinsi": "Jawa Barat",
            "alamat_kode_pos": "12345",
            "no_hp": "0123456789012",
            "pekerjaan": "PNS",
            "status_perkawinan": "",
            "agama": "islam",
        }

        pasien = Pasien.objects.get(id=1)
        waktu_dibuat = pasien.waktu_dibuat.astimezone().isoformat()

        now = timezone.now()
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=now)):
            response = self.client.put(self.url + "1/", data)

        data["id"] = 1
        data["dikelola_oleh"] = [self.pengguna.id]
        data["dibuat_oleh"] = self.pengguna.id
        data["waktu_dibuat"] = waktu_dibuat
        data["diubah_oleh"] = self.pengguna.id
        data["waktu_diubah"] = now.astimezone().isoformat()
        data["diarsipkan"] = False

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_pasien_destroy(self):
        response = self.client.delete(self.url + "1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pasien.objects.count(), 0)


class AppointmentAPITestCase(APITestCase):
    url = "/rekam-medis/perjanjian/"

    def setUp(self):
        pengguna_data = {
            "username": "dimas",
            "password": "asdf1234",
            "nama_panggilan": "Dimas",
            "no_hp": "081122334450",
            "peran": Pengguna.Peran.STAF_ADMINISTRASI,
        }
        self.pengguna = create_pengguna_and_masuk(self.client, pengguna_data)

        self.pasien = Pasien.objects.create(
            nama="Dimas",
            jenis_kelamin="l",
            nama_kk="Dimas",
            tempat_lahir="Depok",
            tanggal_lahir="2000-01-01",
            alamat="Maharaja",
            alamat_rt="001",
            alamat_rw="002",
            alamat_kel_desa="Kel",
            alamat_kecamatan="Kec",
            alamat_kota_kab="Depok",
            alamat_provinsi="Jawa Barat",
            alamat_kode_pos="12345",
            no_hp="0123456789012",
            pekerjaan="Mahasiswa",
            status_perkawinan="belum_menikah",
            agama="islam",
            dibuat_oleh=self.pengguna,
        )
        self.pasien.dikelola_oleh.add(self.pengguna)

    def test_create_only_with_required_fields(self):
        data = {
            "pasien": self.pasien.id,
            "tanggal": "2023-10-02",
            "waktu_mulai": "10:00:00",
            "keluhan": "Gigi sakit untuk menelan",
        }

        now = timezone.now()
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=now)):
            response = self.client.post(self.url, data)

        expected_response = data | {
            "diarsipkan": False,
            "dibuat_oleh": self.pengguna.id,
            "diubah_oleh": self.pengguna.id,
            "dokter_gigi": None,
            "id": 1,
            "nama_pasien": self.pasien.nama,
            "pasien": self.pasien.id,
            "status": Perjanjian.Status.MENUNGGU.value,
            "waktu_dibuat": now.astimezone().isoformat(),
            "waktu_diubah": now.astimezone().isoformat(),
            "waktu_selesai": None,
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pprint.pprint(response.data)
        pprint.pprint(expected_response)
        self.assertEqual(response.data, expected_response)
