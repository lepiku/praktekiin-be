from django.db import models
from django.contrib.auth.models import AbstractUser


class Pengguna(AbstractUser):
    class Peran(models.TextChoices):
        STAF_ADMIN = 'admin', 'Staf Administrasi'
        DOKTER_GIGI = 'dokter_gigi', 'Dokter Gigi'
        PERAWAT = 'perawat', 'Perawat'
        PASIEN = 'pasien', 'Pasien'

    nama_panggilan = models.CharField(max_length=32)
    peran = models.CharField(
        max_length=16,
        blank=True,
        choices=Peran.choices,
        default=Peran.PASIEN)
    no_hp = models.CharField('No. HP', max_length=15)


class JadwalKerja(models.Model):
    pengguna = models.ForeignKey(
        Pengguna,
        related_name='daftar_jadwal_kerja',
        on_delete=models.CASCADE)
    hari = models.PositiveSmallIntegerField()
    waktu_awal = models.TimeField()
    waktu_akhir = models.TimeField()


class Notifikasi(models.Model):
    class Tipe(models.TextChoices):
        PRAKTIK = 'praktik', 'Praktik'
        PERJANJIAN = 'perjanjian', 'Perjanjian'
        PENGUMUMAN = 'pengumuman', 'Pengumuman'
        PASIEN = 'pasien', 'Pasien'

    daftar_penerima = models.ManyToManyField(
        Pengguna, related_name='daftar_notifikasi')
    tipe = models.CharField(max_length=16, choices=Tipe.choices)
    pesan = models.TextField()
    teks_tombol = models.CharField(max_length=64, blank=True)
    url_tombol = models.URLField(blank=True)

    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_notifikasi',
        null=True,
        on_delete=models.SET_NULL)
