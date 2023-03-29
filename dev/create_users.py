from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from akun.models import *
from rekam_medis.models import *

# permissions
crud_pasien = Permission.objects.filter(
    content_type=ContentType.objects.get_for_model(Pasien)
)

# create groups
group_stafadmin, created = Group.objects.get_or_create(name="Staf Administrasi")
if created:
    group_stafadmin.permissions.set(crud_pasien)
group_doktergigi, _ = Group.objects.get_or_create(name="Dokter Gigi")
group_pasien, _ = Group.objects.get_or_create(name="Pasien")

# create users
dimas = {
    "username": "dimas",
    "password": "asdf1234",
    "nama_panggilan": "Dimas",
    "no_hp": "081122334450",
    "peran": Pengguna.Peran.STAF_ADMINISTRASI,
}
if not Pengguna.objects.filter(**dimas).exists():
    p = Pengguna.objects.create_superuser(**dimas)
    p.groups.set([group_stafadmin])

doktergigi = {
    "username": "doktergigi1",
    "password": "asdf1234",
    "nama_panggilan": "Dokter Gigi 1",
    "no_hp": "081122334451",
    "peran": Pengguna.Peran.DOKTER_GIGI,
}
if not Pengguna.objects.filter(**doktergigi).exists():
    p = Pengguna.objects.create_user(**doktergigi)
    p.groups.set([group_doktergigi])

stafadmin = {
    "username": "stafadmin1",
    "password": "asdf1234",
    "nama_panggilan": "Staf Admin 1",
    "no_hp": "081122334452",
    "peran": Pengguna.Peran.STAF_ADMINISTRASI,
}
if not Pengguna.objects.filter(**stafadmin).exists():
    p = Pengguna.objects.create_user(**stafadmin)
    p.groups.set([group_stafadmin])

pasien = {
    "username": "pasien1",
    "password": "asdf1234",
    "nama_panggilan": "Pasien 1",
    "no_hp": "081122334453",
    "peran": Pengguna.Peran.PASIEN,
}
if not Pengguna.objects.filter(**pasien).exists():
    p = Pengguna.objects.create_user(**pasien)
    p.groups.set([group_pasien])
