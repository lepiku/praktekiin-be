from rest_framework import serializers
from akun.models import Pengguna


class PenggunaSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(
        source='get_role_display', read_only=True)

    class Meta:
        model = Pengguna
        fields = ['id', 'username', 'email', 'role', 'role_name']
