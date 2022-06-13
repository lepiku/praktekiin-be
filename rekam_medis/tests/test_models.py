from django.test import TestCase
from rekam_medis.models import Pasien


class PasienModelTest(TestCase):
    def test_pasien_model(self):
        pasien = Pasien.objects.create(
            nama='Dimas',
            nama_kk='Dimas',
            alamat='Depok',
            pekerjaan='Mahasiswa',
            tanggal_lahir='2000-01-01',
            no_telp='0123456789012',
        )

        self.assertEqual(str(pasien), pasien.nama)
