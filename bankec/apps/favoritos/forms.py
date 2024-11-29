from django import forms
from apps.favoritos.models import Favorito
from apps.usuario.models import Usuario


class FavoritoForm(forms.ModelForm):
    class Meta:
        model = Favorito
        fields = ['favorito']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['favorito'].queryset = Usuario.objects.exclude(id=user.id)