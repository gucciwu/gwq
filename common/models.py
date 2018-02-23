from django.contrib.auth.models import User


class UserUtils:
    @staticmethod
    def get_recycle_user():
        return User.objects.get_or_create(username='RECYCLE')[0]

    @staticmethod
    def get_system_user():
        return User.objects.get_or_create(username='SYSTEM')[0]

    @staticmethod
    def get_unknown_user():
        return User.objects.get_or_create(username='UNKNOWN')[0]

    @staticmethod
    def get_user_from_request(request):
        return request.user._wrapped \
            if hasattr(request.user, '_wrapped') \
            else request.user

