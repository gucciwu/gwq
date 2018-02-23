from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view

from base.views import BaseViewSet
from common.models import UserUtils
from .serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from django.core import serializers


class UserViewSet(BaseViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def current(self, request):
        user = UserUtils.get_user_from_request(request)
        self.queryset = User.objects.filter(id=user.id)


class GroupViewSet(BaseViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(['GET'])
def current_user(request):
    """
    API endpoint that fetch current login user.
    """
    user = UserUtils.get_user_from_request(request)
    return Response(serializers.serialize('json', User.objects.filter(id=user.id)))


# current_user = UserViewSet.as_view({'get', 'current'})


