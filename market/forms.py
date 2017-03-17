from django import forms
from .models import Administrador, Diseño


class CreateAccountForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico')
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    contraseña2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Administrador
        fields = ['nombre_empresa', 'email', 'contraseña', 'contraseña2']


class CreateDiseñoForm(forms.ModelForm):
    class Meta:
        model = Diseño
        fields = ['nombres', 'apellidos', 'email', 'archivo_original', 'precio_solicitado']
