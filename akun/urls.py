from django.urls import path
from rest_framework.routers import DefaultRouter

from akun import views

router = DefaultRouter()
router.register(r"dokter-gigi", views.DentistViewSet)

urlpatterns = [
    path(r"masuk/", views.MasukAPIView.as_view(), name="masuk"),
    path(r"keluar/", views.keluar, name="keluar"),
] + router.urls
