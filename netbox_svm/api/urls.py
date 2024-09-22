from netbox.api.routers import NetBoxRouter
from netbox_svm.api.views import (
    NetboxSVMRootView,
    SoftwareProductViewSet,
    SoftwareProductVersionViewSet,
    SoftwareProductInstallationViewSet,
    SoftwareLicenseViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxSVMRootView

router.register("softwareproducts", SoftwareProductViewSet)
router.register("softwareproductversions", SoftwareProductVersionViewSet)
router.register("softwareproductinstallations", SoftwareProductInstallationViewSet)
router.register("softwarelicenses", SoftwareLicenseViewSet)
urlpatterns = router.urls
