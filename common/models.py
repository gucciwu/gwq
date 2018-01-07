from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet
from datetime import datetime


def get_recycle_user():
    return User.objects.get_or_create(username='Recycle')[0]


class BaseQuerySet(QuerySet):
    def delete(self):
        self.update(deleted=True)

    def touch(self, request):
        self.update(modified_by=request.User)
        self.update(modified_time=datetime.now())


class BaseModelManager(models.Manager):
    use_for_related_fields = True

    def with_deleted(self):
        return BaseQuerySet(self.model, using=self._db)

    def deleted(self):
        return self.with_deleted().filter(deleted=True)

    def get_queryset(self):
        return self.with_deleted().exclude(deleted=True)


class BaseModel(models.Model):
    owner = models.ForeignKey(User, related_name='owner_user',
                              on_delete=models.SET(get_recycle_user))

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='create_user',
                                   on_delete=models.SET(get_recycle_user))

    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='modify_user',
                                    on_delete=models.SET(get_recycle_user))

    deleted = models.BooleanField(default=False, editable=False)

    objects = BaseModelManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def force_delete(self, using=None):
        super().delete(self, using)

    class Meta:
        abstract = True


