from netbox.views import generic
from netbox_svm import filtersets, forms, tables, models
from netbox_svm.models import SoftwareProductInstallation
from tenancy.models import Contact
from tenancy.tables import ContactTable
from tenancy.filtersets import ContactFilterSet
from utilities.views import ViewTab, register_model_view
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.utils.translation import gettext as _


class SoftwareProductInstallationListView(generic.ObjectListView):
    """View for listing all existing SoftwareProductInstallations."""
    queryset = SoftwareProductInstallation.objects.all()
    filterset = filtersets.SoftwareProductInstallationFilterSet
    filterset_form = forms.SoftwareProductInstallationFilterForm
    table = tables.SoftwareProductInstallationTable


class SoftwareProductInstallationView(generic.ObjectView):
    """Display SoftwareProductInstallation details"""

    queryset = SoftwareProductInstallation.objects.all()


class SoftwareProductInstallationEditView(generic.ObjectEditView):
    """View for editing and creating a SoftwareProductInstallation instance."""
    queryset = SoftwareProductInstallation.objects.all()
    form = forms.SoftwareProductInstallationForm


class SoftwareProductInstallationDeleteView(generic.ObjectDeleteView):
    """View for deleting a SoftwareProductInstallation instance"""

    queryset = SoftwareProductInstallation.objects.all()


class SoftwareProductInstallationBulkDeleteView(generic.BulkDeleteView):
    queryset = SoftwareProductInstallation.objects.all()
    table = tables.SoftwareProductInstallationTable


@register_model_view(models.SoftwareProductInstallation, 'add_contact', path='contact/add')
class SoftwareProductInstallationAddContactView(generic.ObjectEditView):
    queryset = models.SoftwareProductInstallation.objects.all()
    form = forms.SoftwareProductInstallationAddContactForm
    template_name = 'vewtab_install/installation_add_contact.html'

    def get(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        installation = get_object_or_404(queryset)
        form = self.form(initial=request.GET)

        return render(request, self.template_name, {
            'installation': installation,
            'form': form,
            'return_url': reverse('plugins:netbox_svm:softwareproductinstallation', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        installation = get_object_or_404(queryset)
        form = self.form(request.POST)

        if form.is_valid():

            contact_pks = form.cleaned_data['contact']
            with transaction.atomic():

                # Assign the selected Contact to the installation
                for contact in Contact.objects.filter(pk__in=contact_pks):
                    if contact in installation.contact.all():
                        continue
                    else:
                        installation.contact.add(contact)
                        installation.save()
            messages.success(request, "Added {} contact to installation {}".format(
                len(contact_pks), installation
            ))
            return redirect(installation.get_absolute_url())

        return render(request, self.template_name, {
            'installation': installation,
            'form': form,
            'return_url': installation.get_absolute_url(),
        })

@register_model_view(models.SoftwareProductInstallation, 'contact')
class SoftwareProductInstallationContactView(generic.ObjectChildrenView):
    queryset = models.SoftwareProductInstallation.objects.all()
    child_model = Contact
    table = ContactTable
    filterset = ContactFilterSet
    template_name = 'vewtab_install/installation_remove_contact.html'
    tab = ViewTab(
        label=_('Contact'),
        badge=lambda obj: obj.contact.count() if obj.contact else 0,
        weight=600
    )
     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        contact_list = parent.contact.all()
        return Contact.objects.restrict(request.user, 'view').filter(
            pk__in=[contact.pk for contact in contact_list]
        )

@register_model_view(models.SoftwareProductInstallation, 'remove_contact', path='contact/remove')
class SoftwareProductInstallationRemoveContactView(generic.ObjectEditView):
    queryset = models.SoftwareProductInstallation.objects.all()
    form = forms.SoftwareProductInstallationRemoveContactForm
    template_name = 'netbox_svm/generic/bulk_remove.html'

    def post(self, request, pk):

        installation = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            form = self.form(request.POST)
            # if form.is_valid():
            contact_pks = request.POST.getlist('pk')
            with transaction.atomic():
                    # Remove the selected Contacts from the installation
                    for contact in Contact.objects.filter(pk__in=contact_pks):
                        installation.contact.remove(contact)
                        installation.save()

            messages.success(request, "Removed {} contacts from Installation {}".format(
                len(contact_pks), installation
            ))
            return redirect(installation.get_absolute_url())
        else:
            form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
        pk_values = form.initial.get('pk', [])
        selected_objects = Contact.objects.filter(pk__in=pk_values)
        contact_table = ContactTable(list(selected_objects), orderable=False)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': installation,
            'table': contact_table,
            'obj_type_plural': 'contact',
            'return_url': installation.get_absolute_url(),
        })