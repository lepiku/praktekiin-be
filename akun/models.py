from django.db import models
from django.contrib.auth.models import AbstractUser


class Pengguna(AbstractUser):
    class Role(models.TextChoices):
        STAF_ADMIN = 'ADM', 'Staf Administrasi'
        DOKTER_GIGI = 'DRG', 'Dokter Gigi'
        PERAWAT = 'PRW', 'Perawat'
        PASIEN = 'PAS', 'Pasien'

    nama_panggilan = models.CharField(max_length=32)
    peran = models.CharField(
        max_length=3, blank=True, choices=Role.choices, default=Role.PASIEN)
    no_hp = models.CharField('No. HP', max_length=15)
