from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser
from common.models import UserUtils


def get_content_type_for_model(obj):
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level.
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)


SOFT_DELETION = 4


class BaseViewSet(viewsets.ModelViewSet):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        user = UserUtils.get_user_from_request(self.request)
        instance = serializer.save(owner=user, created_by=user, modified_by=user)
        message = '%s added %s' % (user.username, str(instance))
        self.log_addition(user, instance, message)

    def perform_update(self, serializer):
        instance = serializer.save()
        user = UserUtils.get_user_from_request(self.request)
        instance.modified_by = user
        instance.modified_at = timezone.now()
        instance.save()
        message = '%s changed %s' % (user.username, str(instance))
        self.log_change(user, instance, message)

    def perform_destroy(self, instance):
        instance.deleted = True
        user = UserUtils.get_user_from_request(self.request)
        instance.modified_by = user
        instance.modified_at = timezone.now()
        instance.save(force_update_deleted=True)
        message = '%s soft deleted %s' % (user.username, str(instance))
        self.log_deletion(user, instance, message)

    def log_addition(self, user, object, message):
        """
        Log that an object has been successfully added.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, ADDITION
        return LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=ADDITION,
            change_message=message,
        )

    def log_change(self, user, object, message):
        """
        Log that an object has been successfully changed.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, CHANGE
        return LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=CHANGE,
            change_message=message,
        )

    def log_deletion(self, user, object, message):
        """
        Log that an object has been successfully soft deleted.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        return LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=DELETION,
            change_message=message,
        )

    def log_soft_deletion(self, user, object, message):
        """
        Log that an object has been successfully soft deleted.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        return LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=SOFT_DELETION,
            change_message=message,
        )


class BaseAPIView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)

