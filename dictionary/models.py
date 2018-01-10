from base.models import BaseModel
from django.db import models


class System(BaseModel):
    entry = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.entry + '/' + self.key


class Exchange(BaseModel):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name + '/' + self.code


class SecurityType(BaseModel):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name + '/' + self.code
