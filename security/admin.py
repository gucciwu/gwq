from django.contrib import admin
from .models import Security
from base.admin import BaseModelAdmin


class SecurityModelAdmin(BaseModelAdmin):
    list_display = ('code', 'name') + BaseModelAdmin.list_display


admin.site.register(Security, SecurityModelAdmin)
