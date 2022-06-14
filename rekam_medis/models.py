from django.db import models


class Pasien(models.Model):
    class JenisKelamin(models.TextChoices):
        LAKI_LAKI = 'L', 'Laki-laki'
        PEREMPUAN = 'P', 'Perempuan'

    nama = models.CharField(max_length=256)
    nama_kk = models.CharField(max_length=256)
    alamat = models.CharField(max_length=512)
    pekerjaan = models.CharField(max_length=128)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(
        max_length=1, choices=JenisKelamin.choices)
    no_telp = models.CharField(max_length=20, blank=True)

    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_pasien',
        null=True,
        on_delete=models.SET_NULL)
    waktu_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
