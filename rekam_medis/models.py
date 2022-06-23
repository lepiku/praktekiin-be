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
        'Jenis Kelamin', max_length=1, choices=JenisKelamin.choices)
    nama_kk = models.CharField('Nama Kepala Keluarga', max_length=256)
    tempat_lahir = models.CharField('Tempat Lahir', max_length=32, blank=True)
    tanggal_lahir = models.DateField('Tanggal Lahir')
    nama_ayah_suami = models.CharField(
        'Nama Ayah / Suami', max_length=256, blank=True)
    alamat = models.CharField('Alamat', max_length=512)
    alamat_rt = models.CharField('RT', max_length=5, blank=True)
    alamat_rw = models.CharField('RW', max_length=5, blank=True)
    alamat_kel_desa = models.CharField(
        'Kelurahan / Desa', max_length=32, blank=True)
    alamat_kecamatan = models.CharField('Kecamatan', max_length=32, blank=True)
    alamat_kota_kab = models.CharField(
        'Kota / Kabupaten', max_length=32, blank=True)
    alamat_provinsi = models.CharField('Provinsi', max_length=32, blank=True)
    alamat_kode_pos = models.CharField('Kode Pos', max_length=5, blank=True)
    no_telp = models.CharField('No. Telepon', max_length=20, blank=True)
    pekerjaan = models.CharField('Pekerjaan', max_length=128)
    status_perkawinan = models.CharField(
        'Status Perkawinan',
        max_length=2,
        blank=True,
        choices=StatusPerkawinan.choices,
        default=StatusPerkawinan.KOSONG)
    agama = models.CharField(
        'Agama',
        max_length=10,
        blank=True,
        choices=Agama.choices,
        default=Agama.KOSONG)
    cara_bayar = models.CharField(
        'Cara Pembayaran',
        max_length=1,
        blank=True,
        choices=CaraBayar.choices,
        default=CaraBayar.KOSONG)
    tanggal = models.DateField('Tanggal', null=True)
    promosi = models.BooleanField('Promosi', null=True)

    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_pasien',
        null=True,
        on_delete=models.SET_NULL)
    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    waktu_diubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama
