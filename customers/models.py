from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class Customer(models.Model):
    first_name = models.CharField("First Name", max_length=31)
    last_name = models.CharField("Last Name", max_length=31)
    date_of_birth = models.DateField("Date of Birth")
    currency_balance = models.DecimalField("Currency Balance", max_digits=7, decimal_places=2)
    page_visits = models.IntegerField("Page Visits")


class CustomerOrder(models.Model):
    order_created_date = models.DateField("Order Created Date")
    customer = models.ForeignKey(Customer, models.RESTRICT, related_name="order", verbose_name="Customer")
    item_count = models.IntegerField("Item Count")
    description = models.CharField("Description", max_length=1023)


class AdvertisementItem(models.Model):
    title = models.CharField("Title", max_length=255)
    description = models.CharField("Description", max_length=255)
    how_to_donate = models.CharField("How to Donate", max_length=255)


class HomePage(Page):
    template = "customers/home_page.html"
    page_title = models.CharField("Title", max_length=255, help_text="Enter a page title", default="Home Page")
    description = models.CharField("Description", max_length=255, help_text="Enter a page Description",
                                   default="Test Description")
    content_panels = Page.content_panels + [FieldPanel("page_title")]


class Advertisement(Page):
    template = '/templates/customers/advertisement.html'
    page_title = models.CharField("Title", max_length=255, help_text="Enter an Advertisement Title")
    description = models.CharField("Description", max_length=255, help_text="Enter a Advertisement Description")
    how_to_donate = models.CharField("How to Donate", max_length=255, help_text="Enter a text for guidance")
    content_panels = Page.content_panels + [FieldPanel("page_title"),FieldPanel("description"),FieldPanel("how_to_donate")]


class FlexPage(Page):
    """Home page model."""

    templates = "customers/home_page.html"
    max_count = 1

    banner_title = models.CharField(max_length=100, blank=False, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("banner_title")
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
