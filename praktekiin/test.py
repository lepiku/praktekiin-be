from django.urls import reverse

from akun.models import Pengguna


def create_pengguna_and_masuk(client, pengguna_data):
    pengguna = Pengguna.objects.create_user(**pengguna_data)
    token = client.post(
        reverse("masuk"),
        {
            "username": pengguna_data["username"],
            "password": pengguna_data["password"],
        },
    ).data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return pengguna
