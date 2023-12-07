# adapters.py

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        # Your custom logic here
        if request.tenant.neubit:
            return "/"
        return settings.LOGIN_REDIRECT_URL
