from rest_framework import serializers

from rekam_medis.models import Pasien


class PasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasien
        fields = '__all__'
