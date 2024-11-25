from django import forms
from .models import Transferencia
from apps.usuario.models import Usuario

from ..motivo.models import RazonTransferencia


class TransferForm(forms.ModelForm):
    receptor = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_active=True),
        label="Receptor"
    )
    cantidad = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Cantidad a transferir"
    )
    motivo = forms.ModelChoiceField(
        queryset=RazonTransferencia.objects.all(),
        label="Motivo de la transferencia",
        required=False
    )

    class Meta:
        model = Transferencia
        fields = ['receptor', 'cantidad', 'motivo']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     receptor = cleaned_data.get('receptor')
    #     cantidad = cleaned_data.get('cantidad')
    #
    #     if cantidad is not None and cantidad <= 0:
    #         raise forms.ValidationError("La cantidad debe ser mayor a cero.")
    #
    #     if receptor is None:
    #         raise forms.ValidationError("Debe seleccionar un receptor válido.")
    #
    #     return cleaned_data
