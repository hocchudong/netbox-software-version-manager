from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import safestring

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from .softwareproductinstallation import SoftwareProductInstallation

class SoftwareProduct(NetBoxModel):
    name = models.CharField(max_length=128)
    comments = models.TextField(blank=True)

    description = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.ForeignKey(to="dcim.Manufacturer", on_delete=models.PROTECT, null=True, blank=True)

    objects = RestrictedQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_svm:softwareproduct", kwargs={"pk": self.pk})

    def get_installation_count(self):
        count = SoftwareProductInstallation.objects.filter(software_product_id=self.pk).count()
        return (
            safestring.mark_safe(
                '<a href="{url}">{count}</a>'.format(
                    url=reverse_lazy("plugins:netbox_svm:softwareproductinstallation_list") + f"?q={self.name}",
                    count=count,
                )
            )
            if count
            else "0"
        )
