from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Page

from exampleProject.current_user import get_current_user


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
    class Colours(models.TextChoices):
        RED = "RED", "Red"
        GREEN = "GREEN", "Green"
        BLUE = "BLUE", "Blue"

    title = models.CharField("Title", max_length=255)
    description = models.CharField("Description", max_length=255)
    how_to_donate = models.CharField("How to Donate", max_length=255)
    colour = models.CharField("Colour", max_length=15, choices=Colours.choices, default=Colours.RED)


class HomePage(Page):
    template = "customers/home_page.html"
    page_title = models.CharField("Title", max_length=255, help_text="Enter a page title", default="Home Page")
    description = models.CharField(
        "Description", max_length=255, help_text="Enter a page Description", default="Test Description"
    )
    content_panels = Page.content_panels + [FieldPanel("page_title"), FieldPanel("description")]


class Advertisement(Page):
    template = "/templates/customers/advertisement.html"
    page_title = models.CharField("Title", max_length=255, help_text="Enter an Advertisement Title")
    description = models.CharField("Description", max_length=255, help_text="Enter a Advertisement Description")
    how_to_donate = models.CharField("How to Donate", max_length=255, help_text="Enter a text for guidance")
    content_panels = Page.content_panels + [
        FieldPanel("page_title"),
        FieldPanel("description"),
        FieldPanel("how_to_donate"),
    ]


# ---------------------------Item-------------------------------------------


class Category(models.Model):
    name = models.CharField("Name", max_length=255)
    groups = models.ManyToManyField(Group, verbose_name="Group", related_name="category", blank=True)


class CustomImage(AbstractImage):
    description = models.CharField("Description", max_length=255, blank=True, null=True)
    ref_link = models.URLField("Reference Link", max_length=200, blank=True, null=True)
    bg_color = models.CharField("Background Colour", max_length=7, blank=True, null=True)

    admin_form_fields = Image.admin_form_fields + (
        "description",
        "ref_link",
        "bg_color",
    )


class Item(models.Model):
    name = models.CharField("Name", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="items", verbose_name="Category")
    images = models.ManyToManyField(Image, related_name="item", verbose_name="Images", blank=True)
    visible = models.BooleanField("Visible", default=False)
    price = models.DecimalField("Price", max_digits=7, decimal_places=2)
    description = models.CharField("Description", max_length=1023)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.RESTRICT, related_name="item", verbose_name="Created By", null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = get_current_user()
        super().save(*args, **kwargs)


class Order(models.Model):
    description = models.CharField("Description", max_length=1023)
    items = models.ManyToManyField(Item)


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name="renditions")

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
