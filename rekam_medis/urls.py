from rest_framework.routers import DefaultRouter

from rekam_medis.views import PasienViewSet

router = DefaultRouter()
router.register(r'pasien', PasienViewSet)

urlpatterns = router.urls
