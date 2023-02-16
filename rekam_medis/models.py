from django.db import models


class Pasien(models.Model):
    class JenisKelamin(models.TextChoices):
        LAKI_LAKI = 'l', 'Laki-laki'
        PEREMPUAN = 'p', 'Perempuan'

    class StatusPerkawinan(models.TextChoices):
        BELUM_MENIKAH = 'belum_menikah', 'Belum Menikah'
        SUDAH_MENIKAH = 'sudah_menikah', 'Sudah Menikah'
        JANDA_DUDA = 'janda_duda', 'Janda / Duda'
        KOSONG = '', '-'

    class Agama(models.TextChoices):
        ISLAM = 'islam', 'Islam'
        KATOLIK = 'katolik', 'Katolik'
        PROTESTAN = 'protestan', 'Protestan'
        HINDU = 'hindu', 'Hindu'
        BUDHA = 'budha', 'Budha'
        LAINNYA = 'lainnya', 'Lainnya'
        KOSONG = '', '-'

    nama = models.CharField('Nama Lengkap', max_length=256)
    jenis_kelamin = models.CharField(
        max_length=1, choices=JenisKelamin.choices)
    nama_kk = models.CharField(
        'Nama Kepala Keluarga', max_length=256, blank=True)
    tempat_lahir = models.CharField(max_length=32, blank=True)
    tanggal_lahir = models.DateField()
    alamat = models.CharField(max_length=512)
    alamat_rt = models.CharField('RT', max_length=5, blank=True)
    alamat_rw = models.CharField('RW', max_length=5, blank=True)
    alamat_kel_desa = models.CharField(
        'Kelurahan / Desa', max_length=32, blank=True)
    alamat_kecamatan = models.CharField(max_length=32, blank=True)
    alamat_kota_kab = models.CharField(
        'Kota / Kabupaten', max_length=32, blank=True)
    alamat_provinsi = models.CharField('Provinsi', max_length=32, blank=True)
    alamat_kode_pos = models.CharField('Kode Pos', max_length=5, blank=True)
    no_hp = models.CharField('No. HP', max_length=20, blank=True)
    pekerjaan = models.CharField(max_length=128, blank=True)
    status_perkawinan = models.CharField(
        max_length=16,
        blank=True,
        choices=StatusPerkawinan.choices,
        default=StatusPerkawinan.KOSONG)
    agama = models.CharField(
        max_length=16,
        blank=True,
        choices=Agama.choices,
        default=Agama.KOSONG)
    # TODO pindahin ke model Pengaturan
    #promosi = models.BooleanField(null=True)
    # cara_bayar

    dikelola_oleh = models.ManyToManyField(
        'akun.Pengguna', related_name='mengelola_pasien')
    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_pasien',
        null=True,
        on_delete=models.SET_NULL)
    waktu_diubah = models.DateTimeField(auto_now=True)
    diubah_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='mengubah_pasien',
        null=True,
        on_delete=models.SET_NULL)
    diarsipkan = models.BooleanField(default=False)

    def __str__(self):
        return self.nama


class Perjanjian(models.Model):
    class Status(models.TextChoices):
        MENUNGGU_KONFIRMASI = 'menunggu', 'Menunggu Konfirmasi'
        TERJADWAL = 'terjadwal', 'Terjadwal'
        SELESAI = 'selesai', 'Selesai'

    status = models.CharField(max_length=16, choices=Status.choices)
    pasien = models.ForeignKey(
        Pasien, related_name='daftar_perjanjian', on_delete=models.CASCADE)
    dokter_gigi = models.ForeignKey(
        'akun.Pengguna',
        related_name='daftar_perjanjian',
        null=True,
        on_delete=models.SET_NULL)
    tanggal = models.DateField()
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()
    keluhan = models.TextField()

    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_perjanjian',
        null=True,
        on_delete=models.SET_NULL)
    waktu_diubah = models.DateTimeField(auto_now=True)
    diubah_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='mengubah_perjanjian',
        null=True,
        on_delete=models.SET_NULL)
    diarsipkan = models.BooleanField(default=False)


class RekamMedis(models.Model):
    perjanjian = models.OneToOneField(
        Perjanjian, null=True, on_delete=models.SET_NULL)
    subjective = models.TextField()
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()

    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_rekam_medis',
        null=True,
        on_delete=models.SET_NULL)
    waktu_diubah = models.DateTimeField(auto_now=True)
    diubah_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='mengubah_rekam_medis',
        null=True,
        on_delete=models.SET_NULL)
    diarsipkan = models.BooleanField(default=False)


# Rekam Medis Tambahan
class RekamMedisTambahan(models.Model):
    rekam_medis = models.OneToOneField(
        RekamMedis, primary_key=True, on_delete=models.CASCADE)
    berat = models.PositiveSmallIntegerField()
    daftar_penyakit = models.ManyToManyField(
        'Penyakit', related_name='daftar_rekam_medis_tambahan')
    daftar_alergi = models.ManyToManyField(
        'Alergi', related_name='daftar_rekam_medis_tambahan')


class Penyakit(models.Model):
    nama = models.CharField(max_length=256)
    deskripsi = models.TextField()


class Alergi(models.Model):
    nama = models.CharField(max_length=256)
    deskripsi = models.TextField()


# Objective
class Objective(models.Model):
    rekam_medis = models.ForeignKey(
        RekamMedis, related_name='daftar_objective', on_delete=models.CASCADE)
    regio = models.PositiveSmallIntegerField()
    gigi = models.PositiveSmallIntegerField()
    deskripsi = models.CharField(max_length=256)


# Assessment
class Assessment(models.Model):
    rekam_medis = models.ForeignKey(
        RekamMedis, related_name='daftar_assessment', on_delete=models.CASCADE)
    regio = models.PositiveSmallIntegerField()
    gigi = models.PositiveSmallIntegerField()
    icd10 = models.ForeignKey(
        'ICD10',
        related_name='daftar_assessment',
        verbose_name='ICD10',
        on_delete=models.CASCADE)


class ICD10(models.Model):
    kode = models.CharField(max_length=16, blank=True)
    nama = models.CharField(max_length=256)
    deskripsi = models.TextField(blank=True)


# Plan
class Plan(models.Model):
    class Keterangan(models.TextChoices):
        SELESAI = 'selesai', 'Selesai'
        KONTROL_KEMBALI = 'kontrol_kembali', 'Kontrol Kembali'
        RUJUK = 'rujuk', 'Rujuk'

    rekam_medis = models.ForeignKey(
        RekamMedis, related_name='daftar_plan', on_delete=models.CASCADE)
    resep = models.TextField(blank=True)
    keterangan = models.CharField(max_length=16)
    perjanjian_kontrol_kembali = models.ForeignKey(
        Perjanjian,
        related_name='daftar_plan_kontrol_kembali',
        null=True,
        on_delete=models.SET_NULL)


class PlanTindakan(models.Model):
    plan = models.ForeignKey(
        'Plan', related_name='daftar_plan_tindakan', on_delete=models.CASCADE)
    tindakan = models.ForeignKey(
        'Tindakan',
        related_name='daftar_plan_tindakan',
        on_delete=models.CASCADE)
    regio = models.PositiveSmallIntegerField()
    gigi = models.PositiveSmallIntegerField()
    jumlah = models.PositiveIntegerField()
    biaya = models.PositiveIntegerField()


class Tindakan(models.Model):
    nama = models.CharField(max_length=256)
    harga_min = models.PositiveIntegerField('Harga Minimal')
    harga_maks = models.PositiveIntegerField('Harga Maksimal')
    bagi_hasil = models.PositiveSmallIntegerField()


# Pembayaran
class Pembayaran(models.Model):
    class Metode(models.TextChoices):
        TUNAI = 'tunai', 'Tunai'
        TRANSFER = 'transfer', 'Transfer'
        EDC = 'edc', 'Electronic Data Capture'

    rekam_medis = models.OneToOneField(
        RekamMedis, null=True, on_delete=models.SET_NULL)
    lain_lain = models.PositiveIntegerField('Biaya Lain-lain')
    diskon = models.CharField(max_length=16, blank=True)
    metode = models.CharField(max_length=16, choices=Metode.choices)
    total = models.PositiveIntegerField()
    dicicil = models.BooleanField()

    waktu_dibuat = models.DateTimeField(auto_now_add=True)
    dibuat_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='membuat_pembayaran',
        null=True,
        on_delete=models.SET_NULL)


class PembayaranBagiHasil(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pembayaran', 'plan_tindakan'],
                name='unique_pembayaran_plan_tindakan',
            )
        ]

    pembayaran = models.OneToOneField(
        Pembayaran,
        on_delete=models.CASCADE)
    plan_tindakan = models.OneToOneField(
        PlanTindakan,
        on_delete=models.CASCADE)
    bagi_hasil = models.PositiveSmallIntegerField()


class PembayaranTransfer(models.Model):
    pembayaran = models.OneToOneField(
        Pembayaran, primary_key=True, on_delete=models.CASCADE)
    nama = models.CharField(max_length=256)
    no_rek = models.CharField('No. Rekening', max_length=32)
    dikonfirmasi = models.BooleanField(default=False)
    dikonfirmasi_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='mengonfirmasi_transfer',
        null=True,
        on_delete=models.SET_NULL)
    waktu_dikonfirmasi = models.DateTimeField(null=True)


class PembayaranCicilan(models.Model):
    pembayaran = models.ForeignKey(Pembayaran, on_delete=models.CASCADE)
    biaya = models.PositiveIntegerField()
    dikonfirmasi = models.BooleanField(default=False)
    dikonfirmasi_oleh = models.ForeignKey(
        'akun.Pengguna',
        related_name='mengonfirmasi_cicilan',
        null=True,
        on_delete=models.SET_NULL)
    waktu_dikonfirmasi = models.DateTimeField(null=True)
