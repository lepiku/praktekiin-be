from rest_framework import viewsets

from rekam_medis.models import Pasien
from rekam_medis.serializers import PasienSerializer


class PasienViewSet(viewsets.ModelViewSet):
    queryset = Pasien.objects.all()
    serializer_class = PasienSerializer
