from django.db import models
from django.contrib.auth.models import AbstractUser


class Pengguna(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'AD', 'Admin'
        DOKTER = 'DR', 'Dokter'
        PERAWAT = 'PR', 'Perawat'
        PASIEN = '', 'Pasien'

    role = models.CharField(
        max_length=2, blank=True, choices=Role.choices, default=Role.PASIEN)
