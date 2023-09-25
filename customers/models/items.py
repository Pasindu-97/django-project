from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from wagtail.images.models import AbstractImage, Image, AbstractRendition

from exampleProject.current_user import get_current_user


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
