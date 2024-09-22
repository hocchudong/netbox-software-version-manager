# from netbox.views import generic
# from django.shortcuts import get_object_or_404, redirect, render
# from netbox_svm.models import SoftwareProductVersion, SoftwareLicense

# from .. import forms, tables, filtersets

# from django.db import transaction
# from django.urls import reverse
# from django.utils.translation import gettext as _
# from utilities.views import ViewTab, register_model_view
# from django.contrib import messages


# @register_model_view(SoftwareProductVersion, 'softwareproductlicense')
# class SwLicenseInstallView(generic.ObjectChildrenView):
#     queryset = SoftwareProductVersion.objects.all()
#     child_model = SoftwareProductInstallation
#     table = tables.SoftwareProductInstallationTable
#     filterset = filtersets.SoftwareProductInstallationFilterSet
#     template_name = 'viewtab_version/software_installations.html'

#     # def get_badge(self, obj):
#     #     count = SoftwareProductInstallation.objects.filter(version_id=obj.pk).count()
#     #     return count if count else 0

#     tab = ViewTab(
#         label=_('Installations'),
#         badge=lambda obj: SoftwareProductInstallation.objects.filter(version_id=obj.pk).count(),
#         weight=600
#     )
#      # permission='virtualization.view_virtualmachine',
#     def get_children(self, request, obj):
#         software_install_list = SoftwareProductInstallation.objects.filter(version_id=obj.pk)
#         return SoftwareProductInstallation.objects.restrict(request.user, 'view').filter(
#             pk__in=[soft_install.pk for soft_install in software_install_list]
#         )

# @register_model_view(SoftwareProductVersion, 'remove_softwareproductinstallation', path='softwareproductinstallation/remove')
# class SwVersionInstallRemoveView(generic.ObjectEditView):
#     queryset = SoftwareProductVersion.objects.all()
#     form = forms.SwVersionRemoveInstallForm
#     template_name = 'netbox_svm/generic/bulk_remove.html'

#     def post(self, request, pk):

#         product_version = get_object_or_404(self.queryset, pk=pk)

#         if '_confirm' in request.POST:
#             form = self.form(request.POST)
#             # if form.is_valid():
#             vms_pks = request.POST.getlist('pk')
#             with transaction.atomic():
#                     # Remove the selected VMs from the Project
#                     for vms in VirtualMachine.objects.filter(pk__in=vms_pks):
#                         project.virtualmachine.remove(vms)
#                         project.save()

#             messages.success(request, "Removed {} vms from Project {}".format(
#                 len(vms_pks), project
#             ))
#             return redirect(project.get_absolute_url())
#         else:
#             form = self.form(request.POST, initial={'pk': request.POST.getlist('pk')})
#         pk_values = form.initial.get('pk', [])
#         selected_objects = VirtualMachine.objects.filter(pk__in=pk_values)
#         vms_table = VirtualMachineTable(list(selected_objects), orderable=False)

#         return render(request, self.template_name, {
#             'form': form,
#             'parent_obj': project,
#             'table': vms_table,
#             'obj_type_plural': 'virtualmachine',
#             'return_url': project.get_absolute_url(),
#         })