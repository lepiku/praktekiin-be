from rest_framework import serializers

from rekam_medis.models import Pasien


class PasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasien
        fields = "__all__"
        read_only_fields = [
            "dibuat_oleh",
            "dikelola_oleh",
            "waktu_dibuat",
            "waktu_diubah",
        ]


class SearchSerializer(serializers.Serializer):
    q = serializers.CharField()
