from django.db import models
from django.urls import reverse
from django.utils import safestring

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from utilities.validators import EnhancedURLValidator


class LaxURLField(models.URLField):
    """
    NetBox Custom Field approach, based on utilities.forms.fields.LaxURLField
    Overriding default_validators is needed, as they are always added
    """

    default_validators = [EnhancedURLValidator()]

class SoftwareLicense(NetBoxModel):
    name = models.CharField(max_length=128)
    comments = models.TextField(blank=True)

    description = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=128)
    stored_location = models.CharField(max_length=255, null=True, blank=True)
    stored_location_url = LaxURLField(max_length=1024, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    support = models.BooleanField(default=None, null=True, blank=True)
    license_amount = models.PositiveIntegerField(default=None, null=True, blank=True)

    software_product = models.ForeignKey(to="netbox_svm.SoftwareProduct", on_delete=models.PROTECT)
    version = models.ForeignKey(to="netbox_svm.SoftwareProductVersion", on_delete=models.PROTECT, null=True, blank=True)
    installation = models.ForeignKey(
        to="netbox_svm.SoftwareProductInstallation", on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = RestrictedQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_svm:softwarelicense", kwargs={"pk": self.pk})

    @property
    def stored_location_txt(self):
        if self.stored_location_url and not self.stored_location:
            return "Link"
        return self.stored_location
