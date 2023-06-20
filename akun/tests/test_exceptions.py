from rest_framework import status
from rest_framework.test import APITestCase


class AkunExceptionsTestCase(APITestCase):
    url = "/rekam-medis/pasien/"

    def test_unauthorized(self):
        response = self.client.get(self.url)
        error_detail = response.data["detail"]

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(error_detail.code, "not_authenticated")
        self.assertEqual(str(error_detail), "Token autentikasi tidak diberikan.")

    def test_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token asdf")
        response = self.client.get(self.url)
        error_detail = response.data["detail"]

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(error_detail.code, "authentication_failed")
        self.assertEqual(str(error_detail), "Salah token.")
