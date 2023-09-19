from django.apps import AppConfig
from wagtail.users.apps import WagtailUsersAppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'


class CustomUsersAppConfig(WagtailUsersAppConfig):
    group_viewset = "customers.views.GroupViewSet"
