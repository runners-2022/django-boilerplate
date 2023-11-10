# Django
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework.filters import OrderingFilter

# Third Party
from drf_yasg.utils import swagger_auto_schema

# Bases
from runners.bases.api import mixins
from runners.bases.api.viewsets import GenericViewSet

# Utils
from runners.utils.decorators import swagger_decorator
from runners.utils.searches import AdvancedSearchFilter

# Filters
from runners.apps.users.api.views.filters.index import UserFilter

# Serializers
from runners.apps.users.api.serializers import UserSerializer

# Models
from runners.apps.users.models import User


# Main Section
class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializers = {
        'default': UserSerializer,
    }
    queryset = User.available.all()
    filter_backends = (DjangoFilterBackend, AdvancedSearchFilter, OrderingFilter)
    filterset_class = UserFilter
    search_fields = ('email',)
    ordering_fields = ('point', 'created')

    @swagger_auto_schema(**swagger_decorator(tag=_('유저'),
                                             id=_('리스트 조회'),
                                             # description=_(''),
                                             response={200: UserSerializer}
                                             ))
    def list(self, request, *args, **kwargs):
        user = request.user
        print('user : ', user)

        return super().list(self, request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='객체 조회',
                                             # description='',
                                             response={200: UserSerializer}
                                             ))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='생성',
                                             # description='',
                                             request=UserSerializer,
                                             response={201: 'ok'}
                                             ))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='수정',
                                             # description='',
                                             request=UserSerializer,
                                             response={200: 'ok'}
                                             ))
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(**swagger_decorator(tag='유저',
                                             id='삭제',
                                             # description='',
                                             response={204: 'no content'}))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)
