from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from akun.models import Pengguna

# Modified from: https://learndjango.com/tutorials/django-custom-user-model


class PenggunaCreationForm(UserCreationForm):
    class Meta:
        model = Pengguna
        fields = "__all__"


class PenggunaChangeForm(UserChangeForm):
    class Meta:
        model = Pengguna
        fields = "__all__"


class PenggunaAdmin(UserAdmin):
    add_form = PenggunaCreationForm
    form = PenggunaChangeForm
    model = Pengguna
    list_display = ["username", "peran", "is_superuser"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fieldsets is not None:
            added_fields = self.fieldsets[0][1]["fields"] + (
                "nama_panggilan",
                "peran",
                "no_hp",
            )
            self.fieldsets[0][1]["fields"] = added_fields


admin.site.register(Pengguna, PenggunaAdmin)
