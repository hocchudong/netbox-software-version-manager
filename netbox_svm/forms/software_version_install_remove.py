from netbox_svm.models import SoftwareProductInstallation
from utilities.forms import ConfirmationForm
from django import forms


class SwVersionRemoveInstallForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=SoftwareProductInstallation.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
