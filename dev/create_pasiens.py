# require create_users.py
from rekam_medis.models import Pasien
from akun.models import Pengguna

user = Pengguna.objects.get(username='dimas')
pasien = Pasien.objects.create(
    nama='Okto',
    jenis_kelamin='l',
    nama_kk='Ayahnya Okto',
    tempat_lahir='Depok',
    tanggal_lahir='2000-01-01',
    alamat='Maharaja',
    alamat_rt='001',
    alamat_rw='002',
    alamat_kel_desa='Kel',
    alamat_kecamatan='Kec',
    alamat_kota_kab='Depok',
    alamat_provinsi='Jawa Barat',
    alamat_kode_pos='12345',
    no_hp='0123456789012',
    pekerjaan='Mahasiswa',
    status_perkawinan='belum_menikah',
    agama='islam',
    dibuat_oleh=user,
    diubah_oleh=user,
)
pasien.dikelola_oleh.add(user)
