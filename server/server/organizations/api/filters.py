import django_filters
from django.db.models import Q

from server.organizations.models import Activity


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    # comma-seperate the values before applying filters. used for "in" lookups
    pass


class ActivityFilter(django_filters.FilterSet):
    domain__in = CharInFilter(field_name="domain", lookup_expr="in")
    target_audience = django_filters.CharFilter(method="target_audience_filter")
    tags = django_filters.CharFilter(method="tags_filter")

    class Meta:
        model = Activity
        fields = ["target_audience", "domain__in"]

    def target_audience_filter(self, queryset, name, value):
        if value.isnumeric():
            return queryset.filter(target_audience__contains=int(value))

        query = Q()
        for str_numeric_grade in value.split(","):
            query = query | Q(target_audience__contains=int(str_numeric_grade))

        return queryset.filter(query)

    def tags_filter(self, queryset, name, value):
        return queryset.filter(tags__name__in=value.split(","))
