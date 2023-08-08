from django.contrib import admin

from .models import Pasien, Perjanjian

# Register your models here.
admin.site.register([Pasien, Perjanjian])
