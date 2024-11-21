from netbox.search import SearchIndex, register_search
from .models import SoftwareLicense, SoftwareProduct, SoftwareProductInstallation, SoftwareProductVersion

@register_search
class SoftwareProductIndex(SearchIndex):
    model = SoftwareProduct
    fields = (
        ('name', 100),
        ('comments', 200),
        ('comments', 5000),
    )


@register_search
class SoftwareProductInstallationIndex(SearchIndex):
    model = SoftwareProductInstallation
    fields = (
        ('owner', 100),
        ('ipaddress', 100),
        ('version', 200),
        ('comments', 5000),
        ('software_product', 200),
    )

@register_search
class SoftwareProductVersionIndex(SearchIndex):
    model = SoftwareProductVersion
    fields = (
        ('name', 100),
        ('comments', 5000),
    )

    