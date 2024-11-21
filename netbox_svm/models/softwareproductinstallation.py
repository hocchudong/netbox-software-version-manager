from django.db import models
from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from django.urls import reverse


class SoftwareProductInstallation(NetBoxModel):
    comments = models.TextField(
        blank=True
    )
        
    software_product = models.ForeignKey(
        to="netbox_svm.SoftwareProduct", 
        on_delete=models.PROTECT
    )
    
    version = models.ForeignKey(
        to="netbox_svm.SoftwareProductVersion", 
        on_delete=models.PROTECT
    )
    
    ipaddress = models.ForeignKey(
        to='ipam.IPAddress', 
        related_name='software_installed',
        blank=True,
        default=None,
        on_delete=models.PROTECT
    )
    
    owner = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=''
    )

    objects = RestrictedQuerySet.as_manager()

    def __str__(self):
        return f"{self.ipaddress} ({self.software_product} {self.version}) "

    
    def get_absolute_url(self):
        return reverse("plugins:netbox_svm:softwareproductinstallation", kwargs={"pk": self.pk})

    # @property
    # def resource(self):
    #     # return self.device or self.virtualmachine or self.cluster or self.ipaddress
    #     self.ipaddress

    def render_type(self):
        return "ipaddress"
        