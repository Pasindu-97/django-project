from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from customers.models import Customer, CustomerOrder


class CustomerAdmin(ModelAdmin):
    model = Customer
    base_url_path = 'customeradmin'
    menu_label = 'Customer'
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('id', 'first_name', 'last_name','date_of_birth','currency_balance','page_visits')
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
    list_display = ('id', 'order_created_date', 'customer','item_count','description')
    list_filter = ('customer',)
    search_fields = ('item_count',)


modeladmin_register(CustomerAdmin)
modeladmin_register(CustomerOrderAdmin)
