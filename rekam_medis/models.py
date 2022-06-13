from django.db import models


class Pasien(models.Model):
    nama = models.CharField(max_length=256)
    nama_kk = models.CharField(max_length=256)
    alamat = models.CharField(max_length=512)
    pekerjaan = models.CharField(max_length=128)
    tanggal_lahir = models.DateField()
    no_telp = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nama
