from django.urls import path
from rest_framework.routers import DefaultRouter

from rekam_medis.views import PasienViewSet, search

router = DefaultRouter()
router.register(r"pasien", PasienViewSet)

urlpatterns = router.urls + [
    path("search/", search, name="search"),
]
