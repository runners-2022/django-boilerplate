# Django
import django_filters
from django_filters import CharFilter, BooleanFilter

# Models
from runners.apps.users.models import User


# Main Section
class UserFilter(django_filters.FilterSet):
    username = CharFilter(field_name='username')
    is_test = BooleanFilter(method='is_test_filter')

    class Meta:
        model = User
        fields = ('username', 'is_test')

    def is_test_filter(self, queryset, title, value):
        if value:
            return queryset
        else:
            return queryset
