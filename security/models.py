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

