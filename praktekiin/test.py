from django.urls import reverse
from akun.models import Pengguna


def create_pengguna_and_login(client, login_data):
    Pengguna.objects.create_user(**login_data)
    token = client.post(reverse('login'), login_data).data['token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
