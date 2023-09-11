from django.db import models


class Customer(models.Model):
    first_name = models.CharField("First Name", max_length=31)
    last_name = models.CharField("Last Name", max_length=31)
    date_of_birth = models.DateField("Date of Birth")
    currency_balance = models.DecimalField("Currency Balance", max_digits=7, decimal_places=2)
    page_visits = models.IntegerField("Page Visits")


class CustomerOrder(models.Model):
    order_created_date = models.DateField("Order Created Date")
    customer = models.ForeignKey(Customer,models.RESTRICT,related_name="order", verbose_name="Customer")
    item_count = models.IntegerField("Item Count")
    description = models.CharField("Description", max_length=1023)



