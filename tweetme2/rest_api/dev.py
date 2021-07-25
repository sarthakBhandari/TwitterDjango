from django.conf import settings
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class DevAuthentication(BasicAuthentication):
    def authenticate(self, request):
        qs = User.objects.all()
        user = qs.first()
        return (user, None)