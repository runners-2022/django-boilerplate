# DRF
from rest_framework_nested import routers

# Views
from runners.apps.users.api.views.index import UserViewSet

# Router
router = routers.SimpleRouter(trailing_slash=False)

# Users
router.register('users', UserViewSet)

app_name = 'api'
urlpatterns = router.urls
