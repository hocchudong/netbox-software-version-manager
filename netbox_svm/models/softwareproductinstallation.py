from django.db import models
from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from django.urls import reverse


class SoftwareProductInstallation(NetBoxModel):
    comments = models.TextField(blank=True)

    device = models.ForeignKey(to="dcim.Device", on_delete=models.PROTECT, null=True, blank=True)
    virtualmachine = models.ForeignKey(
        to="virtualization.VirtualMachine", on_delete=models.PROTECT, null=True, blank=True
    )
    cluster = models.ForeignKey(to="virtualization.Cluster", on_delete=models.PROTECT, null=True, blank=True)
    software_product = models.ForeignKey(to="netbox_svm.SoftwareProduct", on_delete=models.PROTECT)
    version = models.ForeignKey(to="netbox_svm.SoftwareProductVersion", on_delete=models.PROTECT)

    objects = RestrictedQuerySet.as_manager()

    def __str__(self):
        return f"{self.pk} ({self.resource})"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_resource",
                check=(
                    models.Q(device__isnull=False, virtualmachine__isnull=True, cluster__isnull=True)
                    | models.Q(device__isnull=True, virtualmachine__isnull=False, cluster__isnull=True)
                    | models.Q(device__isnull=True, virtualmachine__isnull=True, cluster__isnull=False)
                ),
                violation_error_message="Installation requires exactly one resource destination.",
            )
        ]

    def get_absolute_url(self):
        return reverse("plugins:netbox_svm:softwareproductinstallation", kwargs={"pk": self.pk})

    @property
    def resource(self):
        return self.device or self.virtualmachine or self.cluster

    def render_type(self):
        if self.device:
            return "device"
        if self.virtualmachine:
            return "virtualmachine"
        return "cluster"