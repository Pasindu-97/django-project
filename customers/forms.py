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


class ChangeVisibleWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = '<label style="display:block; margin-bottom:10px;">Change Visibility:</label>'
        html += '<div class="btn-group" role="group">'
        html += f'<a href="?visible=1" class="btn btn-primary{" active" if value else ""}">Visible</a>'
        html += f'<a href="?visible=0" class="btn btn-secondary{" active" if not value else ""}">Hidden</a>'
        html += "</div>"
        return html
