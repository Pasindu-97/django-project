import django_filters

from customers.models import Item


class ItemFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(
        field_name="category__name",
    )

    class Meta:
        model = Item
        fields = ["category_name"]
