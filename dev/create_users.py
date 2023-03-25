# create users

from akun.models import *

dimas = {
    'username': 'dimas',
    'password': 'asdf1234',
    'nama_panggilan': 'Dimas',
    'no_hp': '081122334450',
    'peran': Pengguna.Peran.STAF_ADMINISTRASI
}
Pengguna.objects.create_superuser(**dimas)

doktergigi = {
    'username': 'doktergigi1',
    'password': 'asdf1234',
    'nama_panggilan': 'Dokter Gigi 1',
    'no_hp': '081122334451',
    'peran': Pengguna.Peran.DOKTER_GIGI
}
Pengguna.objects.create_user(**doktergigi)

stafadmin = {
    'username': 'stafadmin1',
    'password': 'asdf1234',
    'nama_panggilan': 'Staf Admin 1',
    'no_hp': '081122334452',
    'peran': Pengguna.Peran.STAF_ADMINISTRASI
}
Pengguna.objects.create_user(**stafadmin)

pasien = {
    'username': 'pasien1',
    'password': 'asdf1234',
    'nama_panggilan': 'Pasien 1',
    'no_hp': '081122334453',
    'peran': Pengguna.Peran.PASIEN
}
Pengguna.objects.create_user(**pasien)
