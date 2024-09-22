from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.choices import ButtonColorChoices
from packaging import version


try:
    from netbox.plugins import PluginMenu
    HAVE_MENU = True
except ImportError:
    HAVE_MENU = False
    PluginMenu = PluginMenuItem

menu_buttons = (
    PluginMenuItem(
        link="plugins:netbox_svm:softwareproduct_list",
        link_text="Software Products",
        permissions=["netbox_svm.add_softwareproduct"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_svm:softwareproduct_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_svm.add_softwareproduct"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_svm:softwareproductversion_list",
        link_text="Versions",
        permissions=["netbox_svm.add_softwareproductversion"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_svm:softwareproductversion_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_svm.add_softwareproductversion"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_svm:softwareproductinstallation_list",
        link_text="Installations",
        permissions=["netbox_svm.add_softwareproductinstallation"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_svm:softwareproductinstallation_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_svm.add_softwareproductinstallation"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_svm:softwarelicense_list",
        link_text="Licenses",
        permissions=["netbox_svm.add_softwarelicense"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_svm:softwarelicense_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_svm.add_softwarelicense"],
            ),
        ),
    ),
)


if HAVE_MENU:
    menu = PluginMenu(
        label=f'Software Management',
        groups=(
            ('Software Version Management', menu_buttons),
        ),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    # display under plugins
    menu_items = menu_buttons


