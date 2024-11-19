import django_tables2 as tables
from django.db.models import Count, F

from netbox.tables import NetBoxTable, ToggleColumn, columns
from netbox_svm.models import SoftwareProduct, SoftwareProductVersion, SoftwareProductInstallation, SoftwareLicense


class SoftwareProductTable(NetBoxTable):
    """Table for displaying SoftwareProduct objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    manufacturer = tables.Column(accessor="manufacturer", linkify=True)
    installations = tables.Column(accessor="get_installation_count")

    tags = columns.TagColumn(url_name="plugins:netbox_svm:softwareproduct_list")

    class Meta(NetBoxTable.Meta):
        model = SoftwareProduct
        fields = (
            "pk",
            "name",
            "manufacturer",
            "description",
            "installations",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "manufacturer",
            "description",
            "installations",
            "tags",
        )
        sequence = (
            "manufacturer",
            "name",
            "description",
            "installations",
        )

    def order_installations(self, queryset, is_descending):
        queryset = queryset.annotate(count=Count("softwareproductinstallation__id")).order_by(
            ("-" if is_descending else "") + "count"
        )
        return queryset, True


class SoftwareProductVersionTable(NetBoxTable):
    """Table for displaying SoftwareProductVersion objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    software_product = tables.Column(accessor="software_product", linkify=True)
    manufacturer = tables.Column(accessor="software_product__manufacturer", linkify=True)
    installations = tables.Column(accessor="get_installation_count")

    tags = columns.TagColumn(url_name="plugins:netbox_svm:softwareproductversion_list")

    class Meta(NetBoxTable.Meta):
        model = SoftwareProductVersion
        fields = (
            "pk",
            "name",
            "software_product",
            "manufacturer",
            "release_date",
            "end_of_support",
            "release_type",
            "installations",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "software_product",
            "manufacturer",
            "release_date",
            "installations",
            "tags",
        )
        sequence = (
            "manufacturer",
            "software_product",
            "name",
            "installations",
        )

    def order_installations(self, queryset, is_descending):
        queryset = queryset.annotate(count=Count("softwareproductinstallation__id")).order_by(
            ("-" if is_descending else "") + "count"
        )
        return queryset, True


SOFTWARE_INSTALL_DETAIL_LINK = """
{% if record.pk %}
    <a href="{{ record.get_absolute_url }}">{{ record.ipaddress }}</a>
{% endif %}
"""

SOFTWARE_INSTALL_CONTACTS = """
{% if record.ipaddress.contacts.first %}
    {{ record.owner }}, <a href="{% url 'tenancy:contact' record.ipaddress.contacts.first.contact.id %}">{{ record.ipaddress.contacts.first.contact }}</a>
{% else %}
    {{ record.owner }}
{% endif %}
"""


class SoftwareProductInstallationTable(NetBoxTable):
    """Table for displaying SoftwareProductInstallation objects."""

    pk = ToggleColumn()
    ip = columns.TemplateColumn(
        template_code=SOFTWARE_INSTALL_DETAIL_LINK,
        export_raw=True,
        attrs={'td': {'class': 'text-nowrap'}}
    )

    owner = columns.TemplateColumn(
        template_code=SOFTWARE_INSTALL_CONTACTS,
        export_raw=True,
        attrs={'td': {'class': 'text-nowrap'}}
    )
    software_product = tables.Column(accessor="software_product", linkify=True)
    version = tables.Column(accessor="version", linkify=True)

    tags = columns.TagColumn(url_name="plugins:netbox_svm:softwareproductinstallation_list")

    class Meta(NetBoxTable.Meta):
        model = SoftwareProductInstallation
        fields = (
            "pk",
            "ip",
            "owner",
            "software_product",
            "version",
            "tags",
        )
        default_columns = (
            "pk",
            "ip",
            "owner",
            "software_product",
            "version",
            "tags",
        )
    
    def order_ip(self, queryset, is_descending):
        queryset = queryset.filter(ipaddress__isnull=False).annotate(
            ipaddress_address=F("ipaddress")).order_by(
                "-ipaddress_address" if is_descending else "ipaddress_address"
        )

        return queryset, True


class SoftwareLicenseTable(NetBoxTable):
    """Table for displaying SoftwareLicense objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()

    type = tables.Column()
    stored_location = tables.Column(accessor="stored_location_txt", linkify=lambda record: record.stored_location_url)

    software_product = tables.Column(accessor="software_product", linkify=True)
    version = tables.Column(accessor="version", linkify=True)
    installation = tables.Column(accessor="installation", linkify=True)

    tags = columns.TagColumn(url_name="plugins:netbox_svm:softwarelicense_list")

    class Meta(NetBoxTable.Meta):
        model = SoftwareLicense
        fields = (
            "pk",
            "name",
            "description",
            "type",
            "stored_location",
            "start_date",
            "expiration_date",
            "software_product",
            "version",
            "installation",
            "support",
            "license_amount",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "expiration_date",
            "software_product",
            "installation",
            "tags",
        )

    def render_software_product(self, value, **kwargs):
        return f"{kwargs['record'].software_product.manufacturer.name} - {value}"

    def render_installation(self, **kwargs):
        return f"{kwargs['record'].installation.resource}"
