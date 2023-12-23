from urllib.parse import parse_qs, urlparse

from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from praktekiin.permissions import CustomModelPermissions

from .models import Pasien, Perjanjian
from .serializers import AppointmentSerializer, PasienSerializer, SearchSerializer


class PasienViewSet(viewsets.ModelViewSet):
    queryset = Pasien.objects.all().order_by("-id")
    serializer_class = PasienSerializer
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
        instance.diubah_oleh = request.user
        instance.dikelola_oleh.add(request.user)
        instance.save()
        return super().update(request, *args, **kwargs)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Perjanjian.objects.all().order_by("-id")
    serializer_class = AppointmentSerializer
    permission_classes = [CustomModelPermissions]

    class AppointmentFilter(filters.FilterSet):
        tanggal_exact = filters.DateFilter(field_name="tanggal")
        tanggal = filters.DateFromToRangeFilter()

    filterset_class = AppointmentFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        pasien = serializer.instance
        pasien.dibuat_oleh = request.user
        pasien.diubah_oleh = request.user
        pasien.save()
        serializer = self.get_serializer(pasien)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.diubah_oleh = request.user
        instance.save()
        return super().update(request, *args, **kwargs)


@api_view()
def search(request):
    query = parse_qs(urlparse(request.get_full_path()).query)
    for key in query:
        if len(query[key]) == 1:
            query[key] = query[key][0]

    search = SearchSerializer(data=query)
    search.is_valid(raise_exception=True)

    pasiens = Pasien.objects.filter(nama__contains=search.validated_data["q"])
    serializer = PasienSerializer(pasiens, many=True)
    return Response({"pasien": serializer.data})
