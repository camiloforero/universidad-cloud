from django import forms


class CreateAccountForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    nombre_empresa = forms.CharField(label='Nombre de la empresa')
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    contraseña2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

class CreateProyectoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del proyecto')
    descripción = forms.CharField(label='Descripción del proyecto', widget=forms.Textarea)
    valor_estimado = forms.DecimalField(label='Valor estimado del proyecto')

class CreateDiseñoForm(forms.Form):
    nombres = forms.CharField(label='Nombres')
    apellidos = forms.CharField(label='Apellidos')
    email = forms.EmailField(label='Correo electrónico')
    precio_solicitado = forms.DecimalField(label='Precio solicitado')
    diseño_original = forms.FileField(label='Diseño')
