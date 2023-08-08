from rest_framework import serializers

from rekam_medis.models import Pasien, Perjanjian


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


class AppointmentSerializer(serializers.ModelSerializer):
    nama_pasien = serializers.CharField(source="pasien.nama")
    nama_dokter_gigi = serializers.CharField(source="dokter_gigi.nama_panggilan")

    class Meta:
        model = Perjanjian
        fields = "__all__"
        read_only_fields = [
            "dibuat_oleh",
            "waktu_dibuat",
            "diubah_oleh",
            "waktu_diubah",
        ]
