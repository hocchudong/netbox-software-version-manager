from netbox.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from ..models import SoftwareProductVersion, SoftwareProductInstallation

from .. import forms, tables, filtersets

from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.views import ViewTab, register_model_view
from django.contrib import messages


@register_model_view(SoftwareProductVersion, 'softwareproductinstallation')
class SwVersionInstallView(generic.ObjectChildrenView):
    queryset = SoftwareProductVersion.objects.all()
    child_model = SoftwareProductInstallation
    table = tables.SoftwareProductInstallationTable
    filterset = filtersets.SoftwareProductInstallationFilterSet
    template_name = 'viewtab_version/software_installations.html'

    tab = ViewTab(
        label=_('Installations'),
        badge=lambda obj: SoftwareProductInstallation.objects.filter(version_id=obj.pk).count(),
        weight=600
    )

    def get_children(self, request, obj):
        software_install_list = SoftwareProductInstallation.objects.filter(version_id=obj.pk)
        return SoftwareProductInstallation.objects.restrict(request.user, 'view').filter(
            pk__in=[soft_install.pk for soft_install in software_install_list]
        )