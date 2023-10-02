from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from akun.models import Pengguna
from rekam_medis.models import Pasien, Perjanjian


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


def get_model_permission(model):
    return Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(model)
    )


def set_group(pengguna):
    if pengguna.peran == Pengguna.Peran.STAF_ADMINISTRASI:
        group_stafadmin, _ = Group.objects.get_or_create(name="Staf Administrasi")
        group_stafadmin.permissions.set(
            get_model_permission(Pasien) | get_model_permission(Perjanjian)
        )
        group_stafadmin.permissions
        pengguna.groups.set([group_stafadmin])
