from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import safestring

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from utilities.validators import EnhancedURLValidator
from .softwareproductinstallation import SoftwareProductInstallation

class LaxURLField(models.URLField):
    """
    NetBox Custom Field approach, based on utilities.forms.fields.LaxURLField
    Overriding default_validators is needed, as they are always added
    """

    default_validators = [EnhancedURLValidator()]


class SoftwareReleaseTypes(models.TextChoices):
    ALPHA = "A", "Alpha"
    BETA = "B", "Beta"
    RELEASE_CANDIDATE = "RC", "Release candidate"
    STABLE = "S", "Stable release"


class SoftwareProductVersion(NetBoxModel):
    name = models.CharField(max_length=64)
    comments = models.TextField(blank=True)

    release_date = models.DateField(null=True, blank=True)
    documentation_url = LaxURLField(max_length=1024, null=True, blank=True)
    end_of_support = models.DateField(null=True, blank=True)
    filename = models.CharField(max_length=64, null=True, blank=True)
    file_checksum = models.CharField(max_length=128, null=True, blank=True)
    file_link = LaxURLField(max_length=1024, null=True, blank=True)

    release_type = models.CharField(
        max_length=3,
        choices=SoftwareReleaseTypes.choices,
        default=SoftwareReleaseTypes.STABLE,
    )

    software_product = models.ForeignKey(
        to="netbox_svm.SoftwareProduct",
        on_delete=models.PROTECT,
    )

    objects = RestrictedQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_svm:softwareproductversion", kwargs={"pk": self.pk})

    def get_installation_count(self):
        count = SoftwareProductInstallation.objects.filter(version_id=self.pk).count()
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
