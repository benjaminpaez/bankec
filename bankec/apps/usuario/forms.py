from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class CreationUserForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'dni', 'password1', 'password2']
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni', 'first_name', 'last_name', 'email']

class DepositMoneyForm(forms.Form):
    monto = forms.DecimalField(max_digits=10, decimal_places=2)

