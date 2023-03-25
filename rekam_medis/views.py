from rest_framework import status, viewsets
from rest_framework.response import Response

from rekam_medis.models import Pasien
from rekam_medis.serializers import PasienSerializer
from rest_framework.pagination import PageNumberPagination
from praktekiin.permissions import CustomModelPermissions


class PasienViewSet(viewsets.ModelViewSet):
    class PasienListPagination(PageNumberPagination):
        page_size = 20

    queryset = Pasien.objects.all().order_by("-id")
    serializer_class = PasienSerializer
    pagination_class = PasienListPagination
    permission_classes = [CustomModelPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        pasien = serializer.instance
        pasien.dibuat_oleh = request.user
        pasien.diubah_oleh = request.user
        pasien.save()
        pasien.dikelola_oleh.add(request.user)
        serializer = self.get_serializer(pasien)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.dibuat_oleh is None:
            instance.dibuat_oleh = request.user
            instance.dikelola_oleh.add(request.user)
        instance.diubah_oleh = request.user
        instance.save()
        return super().update(request, *args, **kwargs)
