from django.db.models import F
from rest_framework.filters import OrderingFilter


class NullsLastOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        orderings = self.get_ordering(request, queryset, view)

        if orderings:
            for index, ordering in enumerate(orderings):
                if ordering[0] != '-':
                    orderings[index] = F(ordering).desc(nulls_last=True)
                else:
                    ordering = ordering[1:]
                    orderings[index] = F(ordering).asc(nulls_last=True)
            return queryset.order_by(*orderings)

        return queryset

