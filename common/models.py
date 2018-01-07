from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone


def get_recycle_user():
    return User.objects.get_or_create(username='Recycle')[0]


class BaseQuerySet(QuerySet):
    def delete(self):
        self.update(deleted=True)

    def force_delete(self):
        super().delete()

    def restore(self):
        self.update(deleted=False)

    def update(self, **kwargs):
        self.update(modified_at=timezone.now())
        super().update()

    def touch(self, request):
        self.update(modified_by=request.User)
        self.update(modified_time=timezone.now())


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.modified_at = timezone.now()
        super().save()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def force_delete(self, using=None):
        super().delete(self, using)

    def restore(self):
        self.deleted = False
        self.save()

    class Meta:
        abstract = True