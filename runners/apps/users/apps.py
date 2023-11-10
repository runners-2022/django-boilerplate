# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# Main Section
class UsersConfig(AppConfig):
    name = 'runners.apps.users'
    verbose_name = _('유저')

    def ready(self):
        try:
            import runners.apps.users.signals
        except ImportError:
            pass
