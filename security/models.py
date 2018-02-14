from base.models import BaseModel
from django.db import models
from dictionary.models import SecurityType, Exchange
from django.utils.translation import gettext as _


class Security(BaseModel):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    short_name = models.CharField(max_length=20)
    industry = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    type = models.ForeignKey(SecurityType, on_delete=models.PROTECT)
    exchange = models.ForeignKey(Exchange, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + '/' + self.code

    class Meta:
        db_table = 'security'
        verbose_name = _('security')
        verbose_name_plural = _('securities')


class SecurityTypeUtils:
    @staticmethod
    def stock():
        return SecurityType.objects.get_or_create(code='STOCK')[0]

    @staticmethod
    def option():
        return SecurityType.objects.get_or_create(code='OPTION')[0]

    @staticmethod
    def fund():
        return SecurityType.objects.get_or_create(code='FUND')[0]


class ExchangeUtils:
    @staticmethod
    def shanghai():
        return Exchange.objects.get_or_create(code='SS')[0]

    @staticmethod
    def shenzhen():
        return Exchange.objects.get_or_create(code='SZ')[0]

    @staticmethod
    def hongkong():
        return Exchange.objects.get_or_create(code='HK')[0]