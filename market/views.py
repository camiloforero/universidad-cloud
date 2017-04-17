from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.files.storage import DefaultStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.urls import reverse_lazy
from . import forms, models, tasks

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from vanilla import TemplateView, FormView, CreateView, DetailView
from django.conf import settings

from boto3.dynamodb.conditions import Attr, Key
import botocore

from datetime import datetime


class IndexView(TemplateView):
    template_name = "market/index.html"


class RegistroView(FormView):
    template_name = "market/form.html"
    form_class = forms.CreateAccountForm
    success_url = reverse_lazy('portal:proyectos')

    def form_valid(self, form):
        empresas = settings.TABLA_EMPRESAS
        user = models.User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['contraseña'], is_staff=True)
        try:
            slug_empresa = slugify(
                form.cleaned_data['nombre_empresa']+"-"+str(user.pk),
                allow_unicode=True)
            empresa_data = {
                 'nombre_empresa': form.cleaned_data['nombre_empresa'],
                 'slug_empresa': slug_empresa,
                 'id_usuario': user.id,
                 'proyectos': [],
            }
            try:
                result = empresas.put_item(
                    Item=empresa_data,
                    ConditionExpression=Attr('id_usuario').not_exists()&Attr('slug_empresa').not_exists()
                )
                print(result)
            except botocore.exceptions.ClientError as e:
                print(e)
                if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                    print(e.response['Error']['Message'])
                    raise
                else:
                    raise
            login(self.request, user)
            return super(RegistroView, self).form_valid(form)
        except Exception as e:
            user.delete()
            raise e


class EmpresaHomepageView(TemplateView):
    template_name = "market/empresa_homepage.html"
    lookup_url_kwarg = "slug_empresa"
    def get_context_data(self, **kwargs):
        empresas = settings.TABLA_EMPRESAS
        context = super(EmpresaHomepageView, self).get_context_data(**kwargs)
        empresa = empresas.get_item(
            Key={'slug_empresa': self.kwargs['slug_empresa']}
        )
        context['administrador'] = empresa['Item']
        proyectos_table = settings.DYNAMODB_ENDPOINT.Table('proyectos')
        proyectos = proyectos_table.query(
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('slug_empresa').eq(self.kwargs['slug_empresa'])
        )
        context['proyectos'] = proyectos['Items']
        print(empresa['Item'])
        return context


@method_decorator(csrf_exempt, name='dispatch')
class CrearDiseñoView(FormView):
    template_name = "market/form.html"
    form_class = forms.CreateDiseñoForm

    def form_valid(self, form):
        proyectos_table = settings.DYNAMODB_ENDPOINT.Table('proyectos')
        diseños_table = settings.DYNAMODB_ENDPOINT.Table('disenhos')
        storage = DefaultStorage()
        slug = self.kwargs['slug_empresa']
        n_empresa = self.kwargs['nombre']
        try:
            self.success_url = reverse_lazy(
                'market:homepage',
                kwargs={"slug_empresa": self.kwargs['slug_empresa']}
                )
            diseño_name, diseño_file = list(self.request.FILES.items())[0]
            print(diseño_file)
            diseño_name = storage.save(diseño_file.name, diseño_file)
            id_diseño = "%s###%s" % (slug, n_empresa)
            diseño_item = {
                'id_diseño': id_diseño,
                'fecha_creacion': datetime.now().isoformat(),
                'estado': False,
                'precio_solicitado':form.cleaned_data['precio_solicitado'],
                'archivo_original':storage.url(diseño_name),
                'nombres':form.cleaned_data['nombres'],
                'apellidos':form.cleaned_data['apellidos'],
                'email':form.cleaned_data['email'],
            }

            success = super(CrearDiseñoView, self).form_valid(form)
            result = diseños_table.put_item(
                Item=diseño_item,
                ConditionExpression=Attr('id_diseño').not_exists()|Attr('email').not_exists()
            )
        #try:
            send_mail(
                "Gracias por subir tu diseño, %s" % form.cleaned_data['nombres'],
                "Hemos recibido tu diseño y lo estamos procesando para que sea publicado",
                "ce.forero2551@uniandes.edu.co",
                [form.cleaned_data['email']],
                fail_silently=False
            )
            tasks.convertir_diseño.delay(id_diseño, form.cleaned_data['email'],
            diseño_name, form.cleaned_data['nombres'], form.cleaned_data['apellidos'])
            return success
        except KeyError:
            print("error al enviar el correo")
            #print(e)


# Create your views here.
