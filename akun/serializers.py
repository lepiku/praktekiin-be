from rest_framework import serializers

from akun.models import Pengguna


class PenggunaSerializer(serializers.ModelSerializer):
    peran_nama = serializers.CharField(source="get_peran_display", read_only=True)

    class Meta:
        model = Pengguna
        fields = ["id", "username", "nama_panggilan", "no_hp", "peran", "peran_nama"]
