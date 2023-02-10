from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from akun import views

urlpatterns = [
    path('masuk/', views.MasukAPIView.as_view(), name='masuk'),
    path('keluar/', views.keluar, name='keluar'),
]
