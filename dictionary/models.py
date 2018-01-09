from base.models import BaseModel
from django.db import models


class Dictionary(BaseModel):
    entry = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.entry + '/' + self.key

    class Meta:
        db_table = 'dictionary'


class SecurityType(BaseModel):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name + '/' + self.code

    class Meta:
        db_table = 'security_type'


class Security(BaseModel):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    short = models.CharField(max_length=20)
    type = models.ForeignKey(SecurityType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + '/' + self.code

    class Meta:
        db_table = 'security'



