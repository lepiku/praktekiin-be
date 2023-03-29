from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from akun.models import Pengguna
from akun.serializers import PenggunaSerializer


class MasukAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        pengguna = Pengguna.objects.get(auth_token=response.data["token"])
        serializer = PenggunaSerializer(pengguna)
        response.data["pengguna"] = serializer.data
        return response


@api_view(["POST"])
def keluar(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    request.session.flush()
    return Response({"detail": "Berhasil keluar."})
