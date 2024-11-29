from django import forms
from .models import Transferencia
from apps.usuario.models import Usuario

from ..favoritos.models import Favorito
from ..motivo.models import MotivoTransferencia


class TransferForm(forms.ModelForm):
    receptor = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_active=True),
        label="Receptor",
        required=False
    )
    monto = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Monto"
    )
    motivo = forms.ModelChoiceField(
        queryset=MotivoTransferencia.objects.all(),
        label="Motivo",
        required=True
    )

    # agregar campo para favoritos/sugerencia

    class Meta:
        model = Transferencia
        fields = ['receptor', 'monto', 'motivo']

    def clean(self):
        cleaned_data = super().clean()
        receptor = cleaned_data.get('receptor')
        cantidad = cleaned_data.get('cantidad')

        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a cero.")

        if receptor is None:
            raise forms.ValidationError("Debe seleccionar un receptor válido.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        favoritos = kwargs.pop('favoritos', None)
        super().__init__(*args, **kwargs)
        # if favoritos:
        #     self.fields['receptor_favorito'].queryset = favoritos
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     receptor = cleaned_data.get('receptor')
    #     receptor_favorito = cleaned_data.get('receptor_favorito')
    #
    #     if not receptor or not receptor_favorito:
    #         raise forms.ValidationError("Debes seleccionar un receptor")
    #
    #     if receptor_favorito:
    #         cleaned_data['receptor'] = receptor_favorito
    #     return cleaned_data



