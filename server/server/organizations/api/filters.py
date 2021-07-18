import django_filters

from server.organizations.models import Activity


class ActivityFilter(django_filters.FilterSet):
    target_audience = django_filters.CharFilter(method="target_audience_filter")

    class Meta:
        model = Activity
        fields = ["target_audience"]

    def target_audience_filter(self, queryset, name, value):
        return queryset.filter(target_audience__contains=[value])
