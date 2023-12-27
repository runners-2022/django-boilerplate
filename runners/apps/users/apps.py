# Django
from django.apps import AppConfig


# Main Section
class UsersConfig(AppConfig):
    name = 'runners.apps.users'
    verbose_name = '유저'

    def ready(self):
        try:
            import runners.apps.users.signals
        except ImportError:
            pass
