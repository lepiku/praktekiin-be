from django.test import TestCase
from rekam_medis.models import Pasien


class PasienModelTestCase(TestCase):
    def test_pasien_model_str(self):
        pasien = Pasien.objects.create(
            nama='Dimas',
            nama_kk='Dimas',
            alamat='Depok',
            pekerjaan='Mahasiswa',
            tanggal_lahir='2000-01-01',
            no_hp='0123456789012',
        )

        self.assertEqual(str(pasien), pasien.nama)
