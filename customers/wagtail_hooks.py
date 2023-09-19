from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from customers.models import Customer, CustomerOrder, HomePage, Advertisement, AdvertisementItem, Item, Category, Order


class CustomerAdmin(ModelAdmin):
    model = Customer
    base_url_path = 'customeradmin'
    menu_label = 'Customer'
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'currency_balance', 'page_visits')
    list_filter = ('first_name',)
    search_fields = ('first_name', 'last_name')


class CustomerOrderAdmin(ModelAdmin):
    model = CustomerOrder
    base_url_path = 'customerorderadmin'
    menu_label = 'Customer Order'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('id', 'order_created_date', 'customer', 'item_count', 'description')
    list_filter = ('customer',)
    search_fields = ('item_count',)


class AdvertisementAdmin(ModelAdmin):
    model = AdvertisementItem
    base_url_path = 'advertisementitemadmin'
    menu_label = 'Advertisement'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('id', 'title', 'description', 'how_to_donate')
    list_filter = ('title',)
    search_fields = ('title',)


class OrderAdmin(ModelAdmin):
    model = Order
    base_url_path = 'orderadmin'
    menu_label = 'Order'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('id', 'description', 'items')
    list_filter = ('id',)
    search_fields = ('description',)


class ItemAdmin(ModelAdmin):
    model = Item
    base_url_path = 'itemadmin'
    menu_label = 'Item'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('id', 'name', 'price', 'created_by')
    list_filter = ('name',)
    search_fields = ('name', 'price')


class CategoryAdmin(ModelAdmin):
    model = Category
    base_url_path = 'categoryadmin'
    menu_label = 'Category'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)





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


modeladmin_register(CustomerAdmin)
modeladmin_register(CustomerOrderAdmin)
modeladmin_register(AdvertisementAdmin)
modeladmin_register(ItemAdmin)
modeladmin_register(CategoryAdmin)
modeladmin_register(OrderAdmin)


