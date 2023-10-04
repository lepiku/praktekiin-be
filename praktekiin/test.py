import difflib
import pprint

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from akun.models import Pengguna
from rekam_medis.models import Pasien, Perjanjian


def print_dict_diff(d1, d2):
    print(
        "\n"
        + "\n".join(
            difflib.ndiff(
                pprint.pformat(d1).splitlines(), pprint.pformat(d2).splitlines()
            )
        )
    )


def create_account(account_data):
    account = Pengguna.objects.create_user(**account_data)
    set_group(account)
    return account


def create_account_and_login(client, account_data):
    account = create_account(account_data)

    token = client.post(
        reverse("masuk"),
        {
            "username": account_data["username"],
            "password": account_data["password"],
        },
    ).data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return account


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
