from django.contrib import admin
from .models import Security
from dictionary.models import SecurityType

admin.site.register(Security)
admin.site.register(SecurityType)
