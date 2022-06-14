from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django import forms

from akun.models import Pengguna

# Modified from: https://learndjango.com/tutorials/django-custom-user-model


class PenggunaCreationForm(UserCreationForm):
    class Meta:
        model = Pengguna
        fields = '__all__'


class PenggunaChangeForm(UserChangeForm):
    class Meta:
        model = Pengguna
        fields = '__all__'


class PenggunaAdmin(UserAdmin):
    add_form = PenggunaCreationForm
    form = PenggunaChangeForm
    model = Pengguna
    list_display = ['username', 'role', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fieldsets is not None:
            added_role = self.fieldsets[0][1]['fields'] + ('role',)
            self.fieldsets[0][1]['fields'] = added_role
        if self.add_fieldsets is not None:
            added_role = self.add_fieldsets[0][1]['fields'] + ('role',)
            self.add_fieldsets[0][1]['fields'] = added_role


admin.site.register(Pengguna, PenggunaAdmin)
