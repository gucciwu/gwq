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



