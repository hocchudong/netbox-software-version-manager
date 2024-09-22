from netbox.plugins import PluginTemplateExtension
from .models import SoftwareProductInstallation


class SoftwareVersionInfoExtension(PluginTemplateExtension):
    # def right_page(self):
    #     object = self.context.get('object')
    #     software_version = SoftwareProductInstallation.objects.filter(**{self.kind:object})
    #     return self.render('netbox_svm/inc/software_version_info.html', extra_context={
    #         'software_version': software_version,
    #     })

    # def left_page(self):
    #     object = self.context.get('object')
    #     software_version = SoftwareProductInstallation.objects.filter(**{self.kind:object})
    #     return self.render('netbox_svm/inc/software_version_info.html', extra_context={
    #         'software_version': software_version,
    #     })
    def full_width_page(self):
        object = self.context.get('object')
        software_version = SoftwareProductInstallation.objects.filter(**{self.kind:object})
        return self.render('netbox_svm/inc/software_version_info.html', extra_context={
            'software_version': software_version,
        })

class VirtualMachineSofwareVersionInfo(SoftwareVersionInfoExtension):
    model = 'virtualization.virtualmachine'
    kind = 'virtualmachine'

    # def left_page(self):
    #     return ""

class DeviceSofwareVersionInfo(SoftwareVersionInfoExtension):
    model = 'dcim.device'
    kind = 'device'

    # def right_page(self):
    #     return ""

template_extensions = (
    VirtualMachineSofwareVersionInfo,
    DeviceSofwareVersionInfo
)