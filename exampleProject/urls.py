from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from customers.views import (
    CategoryViewSet,
    CustomerOrderViewSet,
    CustomerViewSet,
    CustomImageViewSet,
    ItemViewSet,
    advertisement_detail,
    advertisement_list,
    home,
    view_orders,
)
from users.views import LoginView, SetPasswordView, UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Example API",
        default_version="v1",
        description="The example project for tutorial",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="pasindu@test.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"customer-orders", CustomerOrderViewSet)
router.register("items", ItemViewSet)
router.register("category", CategoryViewSet)
router.register("image", CustomImageViewSet)
router.register("user", UserViewSet)

urlpatterns = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("home/", home, name="home"),
    path("advertisement", advertisement_list, name="advertisements"),
    path("view_orders/<int:customer_id>/", view_orders, name="view_orders"),
    path("advertisement/<int:advertisement_id>/", advertisement_detail, name="advertisement_detail"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/set_password/", SetPasswordView.as_view(), name="login"),
    path("api/", include(router.urls)),
]
