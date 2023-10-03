from django.urls import path
from rest_framework.routers import DefaultRouter

from rekam_medis.views import AppointmentViewSet, PasienViewSet, search

router = DefaultRouter()
router.register(r"pasien", PasienViewSet)
router.register(r"perjanjian", AppointmentViewSet)

urlpatterns = [
    path("search/", search, name="search"),
] + router.urls
