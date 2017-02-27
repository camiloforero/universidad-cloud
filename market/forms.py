from django import forms
from .models import Administrador


class CreateAccountForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico')
    contraseña = forms.CharField(label='Contraseña')
    contraseña2 = forms.CharField(label='Confirmar contraseña')

    class Meta:
        model = Administrador
        fields = ['nombre_empresa', 'email', 'contraseña', 'contraseña2']
        widgets = {
            'contraseña': forms.PasswordInput(),
            'contraseña2': forms.PasswordInput(),
        }
