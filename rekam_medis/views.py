from rest_framework import status, viewsets
from rest_framework.response import Response

from rekam_medis.models import Pasien
from rekam_medis.serializers import PasienSerializer
from rest_framework.pagination import PageNumberPagination


class PasienListPagination(PageNumberPagination):
    page_size = 20


class PasienViewSet(viewsets.ModelViewSet):
    queryset = Pasien.objects.all().order_by('-id')
    serializer_class = PasienSerializer
    pagination_class = PasienListPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        pasien = serializer.instance
        pasien.dibuat_oleh = request.user
        pasien.save()
        serializer = self.get_serializer(pasien)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.dibuat_oleh is None:
            instance.dibuat_oleh = request.user
        instance.save()
        return super().update(request, *args, **kwargs)
