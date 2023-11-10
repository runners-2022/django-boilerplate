from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend as DrfFilter
from rest_framework.viewsets import GenericViewSet
from url_filter.integrations.drf import DjangoFilterBackend as UrlFilter

from runners.bases.api import mixins
from runners.utils.paginations import StandardResultsSetPagination


class MultiSerializerMixin:
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        if self.serializers and self.serializers['default']:
            return self.serializers.get(self.action, self.serializers['default'])
        else:
            return super().get_serializer_class()


class ModelViewSet(MultiSerializerMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DrfFilter, UrlFilter]
    ordering_fields = "__all__"


class GenericViewSet(MultiSerializerMixin,
                     GenericViewSet):
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DrfFilter, UrlFilter]
    ordering_fields = "__all__"
