from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone
from common.models import UserUtils
from .exceptions import Error
from django.utils.translation import gettext as _


# exceptions
class UpdateWithoutTouchError(Error):
    def __init__(self, message):
        self.message = message


class UpdateDeletedError(Error):
    def __init__(self, message):
        self.message = message


class BaseQuerySet(QuerySet):

    """
    For keeping modified, created and own fields correctly, query set must be touched b4 perform update operations,
    that a flag for judge the queryset have been touched before delete, update and restore
    """
    touched = False

    def delete(self):
        if not self.touched:
            raise UpdateWithoutTouchError(_("QuerySet must be touched before delete!"))
        self.update(deleted=True, modified_at=timezone.now())
        self.touched = False

    def force_delete(self):
        super().delete()

    def restore(self):
        if not self.touched:
            raise UpdateWithoutTouchError(_("QuerySet must be touched before restore!"))
        self.update(deleted=False, modified_at=timezone.now())
        self.touched = False

    def update(self, **kwargs):
        if not self.touched:
            raise UpdateWithoutTouchError(_("QuerySet must be touched before update!"))
        super().update(**kwargs)
        self.touched = False

    def create(self, **kwargs):
        if not self.touched:
            raise UpdateWithoutTouchError(_("QuerySet must be touched before create!"))
        super().create()
        self.touched = False

    def touch(self, user=None, include_create=False, include_owner=False):
        if user is None:
            user = UserUtils.get_unknown_user()

        if include_create:
            if include_owner:
                self.update(modified_time=timezone.now(), modified_by=user,
                            created_time=timezone.now(), created_by=user,
                            owner=user)
            else:
                self.update(modified_time=timezone.now(), modified_by=user,
                            created_time=timezone.now(), created_by=user,
                            )
        else:
            if include_owner:
                self.update(modified_time=timezone.now(), modified_by=user, owner=user)
            else:
                self.update(modified_time=timezone.now(), modified_by=user)

        self.touched = True


class BaseModelManager(models.Manager):
    use_for_related_fields = True

    def with_deleted(self):
        return BaseQuerySet(self.model, using=self._db)

    def deleted(self):
        return self.with_deleted().filter(deleted=True)

    def get_queryset(self):
        return self.with_deleted().exclude(deleted=True)


class BaseModel(models.Model):
    owner = models.ForeignKey(User,
                              related_name="%(app_label)s_%(class)s_owner_related",
                              related_query_name="%(app_label)s_%(class)ss_owner",
                              on_delete=models.SET(UserUtils.get_recycle_user))

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name="%(app_label)s_%(class)s_created_related",
                                   related_query_name="%(app_label)s_%(class)ss_created",
                                   on_delete=models.SET(UserUtils.get_recycle_user))

    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User,
                                    related_name="%(app_label)s_%(class)s_modified_related",
                                    related_query_name="%(app_label)s_%(class)ss_modified",
                                    on_delete=models.SET(UserUtils.get_recycle_user))

    deleted = models.BooleanField(default=False, editable=False)

    objects = BaseModelManager()

    """
    Update modified_by and modified_at without save
    """
    def _soft_touch(self, by_user=None):
        self.modified_at = timezone.now()
        if by_user is not None:
            self.modified_by = by_user
        if self.modified_by is None:
            self.modified_by = UserUtils.get_unknown_user()

    """
    Update modified_by and modified_at fields, save immediately
    """
    def touch(self, by_user=None, force_update_deleted=False):
        if self.deleted and not force_update_deleted:
            return

        self._soft_touch(by_user)
        self.save(update_fields=('modified_by', 'modified_at'))

    """
    For safety, the deleted instance should never update,
    but it can be force update by set @force_update_deleted with True
    """
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, force_update_deleted=False):

        if self.deleted and not force_update_deleted:
            return

        self._soft_touch()

        # set created_at and created_by in creating
        if self._get_pk_val is None:
            self.created_at = timezone.now()
            if self.created_by is None:
                self.created_by = UserUtils.get_unknown_user()

        super().save()

    def delete(self, using=None, keep_parents=False):
        self._soft_touch()
        self.deleted = True
        super().save(update_fields=('modified_by', 'modified_at', 'deleted'))

    def force_delete(self, using=None):
        super().delete(self, using)

    def restore(self):
        self._soft_touch()
        self.deleted = False
        super().save(update_fields=('modified_by', 'modified_at', 'deleted'))

    def set_user(self, user=None):
        if user is None:
            user = UserUtils.get_unknown_user()
        self.owner = user
        self.created_by = user
        self.modified_by = user

    class Meta:
        abstract = True

