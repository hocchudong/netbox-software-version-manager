from dcim.models import Manufacturer
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from netbox_svm.models import SoftwareProduct
from utilities.forms.fields import CommentField, DynamicModelChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet
from netbox.forms import NetBoxModelImportForm
from django import forms

class SoftwareProductForm(NetBoxModelForm):
    """Form for creating a new SoftwareProduct object."""

    comments = CommentField()

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
    )

    class Meta:
        model = SoftwareProduct
        fields = (
            "name",
            "description",
            "manufacturer",
            "tags",
            "comments",
        )


class SoftwareProductFilterForm(NetBoxModelFilterSetForm):
    model = SoftwareProduct
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)

class SoftwareProductImportForm(NetBoxModelImportForm):
    manufacturer = forms.CharField(
        max_length=255,
        required=True,
        help_text="Manufacturer Name. If Manufacture not found it will be set Null as default"
    )

    def clean_manufacturer(self):
        manufacturer=self.cleaned_data.get('manufacturer')
        try:
            manufacturer = Manufacturer.objects.get(name=manufacturer)
            return manufacturer
        except: 
            return None

    class Meta:
        model = SoftwareProduct
        fields = ('name', 'manufacturer', 'description', 'comments')

