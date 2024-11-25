from django.forms import ValidationError
from django.urls import reverse_lazy
from ipam.models import IPAddress
from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from netbox_svm.models import SoftwareProductInstallation, SoftwareProduct, SoftwareProductVersion
from utilities.forms.fields import CommentField, DynamicModelChoiceField, TagFilterField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet
from utilities.forms.widgets import APISelect
from netbox.forms import NetBoxModelImportForm


class SoftwareProductInstallationForm(NetBoxModelForm):
    """Form for creating a new SoftwareProductInstallation object."""

    comments = CommentField()

    ipaddress = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(), 
        required=True,
        selector=True,
        query_params={
            'site_id': ['$site', 'null']
        },
    )
    
    owner = forms.CharField(
        required=False
    )

    software_product = DynamicModelChoiceField(
        queryset=SoftwareProduct.objects.all(),
        required=True,
        widget=APISelect(attrs={"data-url": reverse_lazy("plugins-api:netbox_svm-api:softwareproduct-list")}),
    )
    version = DynamicModelChoiceField(
        queryset=SoftwareProductVersion.objects.all(),
        required=True,
        widget=APISelect(attrs={"data-url": reverse_lazy("plugins-api:netbox_svm-api:softwareproductversion-list")}),
        query_params={
            "software_product": "$software_product",
        },
    )

    class Meta:
        model = SoftwareProductInstallation
        fields = (
            "ipaddress",
            "software_product",
            "owner",
            "version",
            "tags",
            "comments",
        )

    def clean_version(self):
        version = self.cleaned_data["version"]
        software_product = self.cleaned_data["software_product"]
        if version not in software_product.softwareproductversion_set.all():
            raise ValidationError(
                f"Version '{version}' doesn't exist on {software_product}, make sure you've "
                f"selected a compatible version or first select the software product."
            )
        return version


class SoftwareProductInstallationFilterForm(NetBoxModelFilterSetForm):
    model = SoftwareProductInstallation
    fieldsets = (FieldSet(None, ("q", "tag")),)
    tag = TagFilterField(model)


class SoftwareProductInstallationImportForm(NetBoxModelImportForm):
    ipaddress = forms.CharField(
        max_length=255,
        required=True,
        help_text="IPAddress with mask (eg: 10.0.0.100/24)"
    )

    software_product = forms.CharField(
        max_length=255,
        required=True,
        help_text="SoftwareProduct name"
    )

    version = forms.CharField(
        max_length=255,
        required=True,
        help_text="Software version"
    )

    def clean_software_product(self):
        software_product=self.cleaned_data.get('software_product')
        try:
            software_product = SoftwareProduct.objects.get(name=software_product)
            return software_product
        except: 
            raise forms.ValidationError(f"{software_product} not found")

    def clean_version(self):
        version=self.cleaned_data.get('version')
        software_product=self.cleaned_data.get('software_product')
        try:
            version = SoftwareProductVersion.objects.get(software_product__name=software_product,name=version)
            return version
        except: 
            raise forms.ValidationError(f"{version} {software_product} not found")

    def clean_ipaddress(self):
        ipaddress=self.cleaned_data.get('ipaddress')
        try:
            ipaddress = IPAddress.objects.get(address=ipaddress)
            return ipaddress
        except: 
            raise forms.ValidationError(f"{ipaddress} not found")

    class Meta:
        model = SoftwareProductInstallation
        fields = ('ipaddress', 'comments', 'software_product', 'version', 'owner')

