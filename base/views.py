from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser
from common.models import UserUtils


class BaseViewSet(viewsets.ModelViewSet):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        user = UserUtils.get_use_from_request(self.request)
        serializer.save(owner=user,
                        created_by=user,
                        modified_by=user)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.modified_by = UserUtils.get_use_from_request(self.request)
        instance.modified_at = timezone.now()
        instance.save()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.modified_by = UserUtils.get_use_from_request(self.request)
        instance.modified_at = timezone.now()
        instance.save(force_update_deleted=True)


class BaseAPIView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)

