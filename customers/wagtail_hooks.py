from django.shortcuts import render
from django.urls import path
from wagtail import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from customers.authentication import create_user, delete_user
from customers.models import (
    Advertisement,
    AdvertisementItem,
    Category,
    Customer,
    CustomerOrder,
    HomePage,
    Item,
    Order,
)


class CustomerAdmin(ModelAdmin):
    model = Customer
    base_url_path = "customeradmin"
    menu_label = "Customer"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ("id", "first_name", "last_name", "date_of_birth", "currency_balance", "page_visits")
    list_filter = ("first_name",)
    search_fields = ("first_name", "last_name")


class CustomerOrderAdmin(ModelAdmin):
    model = CustomerOrder
    base_url_path = "customerorderadmin"
    menu_label = "Customer Order"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ("id", "order_created_date", "customer", "item_count", "description")
    list_filter = ("customer",)
    search_fields = ("item_count",)


class AdvertisementAdmin(ModelAdmin):
    model = AdvertisementItem
    base_url_path = "advertisementitemadmin"
    menu_label = "Advertisement"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ("id", "title", "description", "how_to_donate")
    list_filter = ("title",)
    search_fields = ("title",)


class OrderAdmin(ModelAdmin):
    model = Order
    base_url_path = "orderadmin"
    menu_label = "Order"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ("id", "description", "items")
    list_filter = ("id",)
    search_fields = ("description",)


class ItemAdmin(ModelAdmin):
    model = Item
    base_url_path = "itemadmin"
    menu_label = "Item"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ("id", "name", "price", "created_by")
    list_filter = ("name",)
    search_fields = ("name", "price")
    form_fields_exclude = ["visible", "created_by"]

    def edit_view(self, request, instance_pk):
        item = Item.objects.get(id=instance_pk)
        if item.created_by != request.user:
            kwargs = {"model_admin": self, "instance_pk": instance_pk}
            view_class = self.edit_view_class
            return view_class.as_view(**kwargs)(request)
        return render(request, "wagtailadmin/page/edit.html")


@hooks.register("register_admin_urls")
def urlpattern():
    return [
        path("item", admin_view, name="visibility"),
    ]


def admin_view(request):
    item_id = request.GET.get("pk")
    item = Item.objects.get(id=item_id)
    item.visible = not item.visible
    item.save()

    context = {
        "instance": item,
    }

    return render(request, "wagtailadmin/page/edit.html", context)


class CategoryAdmin(ModelAdmin):
    model = Category
    base_url_path = "categoryadmin"
    menu_label = "Category"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


class CustomerListPageModelAdmin:
    model = HomePage
    menu_label = "Home Page"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False


class AdvertisementListPageModelAdmin:
    model = Advertisement
    menu_label = "Advertisement Page"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False


@hooks.register("after_create_user")
def do_after_create_user(request, user):
    create_user(user.username)


@hooks.register("after_delete_user")
def do_after_delete_user(request, user):
    delete_user(user.username)


modeladmin_register(CustomerAdmin)
modeladmin_register(CustomerOrderAdmin)
modeladmin_register(AdvertisementAdmin)
modeladmin_register(ItemAdmin)
modeladmin_register(CategoryAdmin)
modeladmin_register(OrderAdmin)
