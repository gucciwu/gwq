from django.contrib import admin
from django.utils import timezone

from common.models import UserUtils
from entry.settings import ADMIN_SITE


class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('owner',
                    'created_at', 'created_by',
                    'modified_at', 'modified_by',
                    'deleted', '__str__')
    list_display_links = ['__str__']

    def extend_list(self, extends=None):
        if extends is not None:
            self.list_display = ('__str__', ) + \
                                extends + \
                                ('created_at', 'created_by',
                                 'modified_at', 'modified_by', 'deleted')

    def save_model(self, request, obj, form, change):
        user = UserUtils.get_use_from_request(request)
        obj.modified_by = user
        obj.modified_at = timezone.now()

        if not change:
            obj.owner = user
            obj.created_by = user
            obj.created_at = timezone.now()

        super().save_model(request, obj, form, change)


admin.site.site_header = ADMIN_SITE['site_header']
admin.site.site_title = ADMIN_SITE['site_title']

