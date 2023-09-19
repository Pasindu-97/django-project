from django import forms

from wagtail.users.forms import GroupForm as WagtailGroupForm

from customers.models import Category


class GroupForm(WagtailGroupForm):
    categories = forms.ModelMultipleChoiceField(
        label="Categories",
        required=False,
        queryset=Category.objects.order_by("name"),
    )

    class Meta(WagtailGroupForm.Meta):
        fields = WagtailGroupForm.Meta.fields + ("categories",)

    def __init__(self, initial=None, instance=None, **kwargs):
        if instance is not None:
            if initial is None:
                initial = {}
            initial["categories"] = instance.categories.all()
        super().__init__(initial=initial, instance=instance, **kwargs)

    def save(self, commit=True):
        instance = super().save()
        instance.categories.set(self.cleaned_data["categories"])
        return instance
