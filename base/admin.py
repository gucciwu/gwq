from django.contrib import admin
from entry.settings import ADMIN_SITE


class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('owner',
                    'created_at', 'created_by',
                    'modified_at', 'modified_by',
                    'deleted', '__str__')

    def extend_list(self, extends=None):
        if extends is not None:
            self.list_display = ('__str__', ) + \
                                extends + \
                                ('created_at', 'created_by',
                                 'modified_at', 'modified_by', 'deleted')


admin.site.site_header = ADMIN_SITE['site_header']
admin.site.site_title = ADMIN_SITE['site_title']

