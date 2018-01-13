from django.contrib import admin
from .models import System, Exchange, SecurityType
from base.admin import BaseModelAdmin


class ExchangeModelAdmin(BaseModelAdmin):
    list_display = ('code', 'name', 'country') + BaseModelAdmin.list_display


class SystemModelAdmin(BaseModelAdmin):
    list_display = ('entry', 'key', 'value') + BaseModelAdmin.list_display


class SecurityTypeModelAdmin(BaseModelAdmin):
    list_display = ('code', 'name') + BaseModelAdmin.list_display
    list_editable = ['name']


admin.site.register(Exchange, ExchangeModelAdmin)
admin.site.register(System, SystemModelAdmin)
admin.site.register(SecurityType, SecurityTypeModelAdmin)
