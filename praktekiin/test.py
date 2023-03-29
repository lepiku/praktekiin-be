from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from akun.models import Pengguna
from rekam_medis.models import Pasien


def create_pengguna_and_masuk(client, pengguna_data):
    pengguna = Pengguna.objects.create_user(**pengguna_data)
    set_group(pengguna)

    token = client.post(
        reverse("masuk"),
        {
            "username": pengguna_data["username"],
            "password": pengguna_data["password"],
        },
    ).data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return pengguna


def set_group(pengguna):
    if pengguna.peran == Pengguna.Peran.STAF_ADMINISTRASI:
        crud_pasien = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Pasien)
        )
        group_stafadmin, _ = Group.objects.get_or_create(name="Staf Administrasi")
        group_stafadmin.permissions.set(crud_pasien)
        pengguna.groups.set([group_stafadmin])
