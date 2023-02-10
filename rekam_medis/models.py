from django.db import models


class Pasien(models.Model):
    class JenisKelamin(models.TextChoices):
        LAKI_LAKI = 'L', 'Laki-laki'
        PEREMPUAN = 'P', 'Perempuan'

    class StatusPerkawinan(models.TextChoices):
        BELUM = 'BL', 'Belum Menikah'
        MENIKAH = 'SD', 'Menikah'
        JANDA_DUDA = 'JD', 'Janda / Duda'
        KOSONG = '', '-'

    class Agama(models.TextChoices):
        ISLAM = 'islam', 'Islam'
        KATOLIK = 'katolik', 'Katolik'
        PROTESTAN = 'protestan', 'Protestan'
        HINDU = 'hindu', 'Hindu'
        BUDHA = 'budha', 'Budha'
        LAINNYA = 'lainnya', 'Lainnya'
        KOSONG = '', '-'

    class CaraBayar(models.TextChoices):
        TUNAI = 'C', 'Tunai'
        TRANSFER = 'T', 'Transfer'
        KOSONG = '', '-'

    nama = models.CharField('Nama Lengkap', max_length=256)
    jenis_kelamin = models.CharField(
        max_length=1, choices=JenisKelamin.choices)
    nama_kk = models.CharField(
        'Nama Kepala Keluarga', max_length=256, blank=True)
    tempat_lahir = models.CharField(max_length=32, blank=True)
    tanggal_lahir = models.DateField()
    alamat = models.CharField('Alamat', max_length=512)
    alamat_rt = models.CharField('RT', max_length=5, blank=True)
    alamat_rw = models.CharField('RW', max_length=5, blank=True)
    alamat_kel_desa = models.CharField(
        'Kelurahan / Desa', max_length=32, blank=True)
    alamat_kecamatan = models.CharField(max_length=32, blank=True)
    alamat_kota_kab = models.CharField(
        'Kota / Kabupaten', max_length=32, blank=True)
    alamat_provinsi = models.CharField(max_length=32, blank=True)
    alamat_kode_pos = models.CharField(max_length=5, blank=True)
    no_hp = models.CharField('No. HP', max_length=20, blank=True)
    pekerjaan = models.CharField(max_length=128, blank=True)
    status_perkawinan = models.CharField(
        max_length=2,
        blank=True,
        choices=StatusPerkawinan.choices,
        default=StatusPerkawinan.KOSONG)
    agama = models.CharField(
        max_length=10,
        blank=True,
        choices=Agama.choices,
        default=Agama.KOSONG)
    promosi = models.BooleanField(null=True)

    dikelola_oleh = models.ManyToManyField(
        'akun.Pengguna', related_name='mengelola_pasien')
    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_pasien',
        null=True,
        on_delete=models.SET_NULL)
    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    waktu_diubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama
