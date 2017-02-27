from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.urls import reverse_lazy
from . import forms, models

from vanilla import TemplateView, FormView, CreateView, DetailView


class IndexView(TemplateView):
    template_name = "market/index.html"


class RegistroView(FormView):
    template_name = "market/form.html"
    form_class = forms.CreateAccountForm
    success_url = reverse_lazy('design_match_admin:index')

    def form_valid(self, form):
        user = models.User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['contraseña'], is_staff=True)
        try:
            group = Group.objects.get(name='DsAdmin')
            user.groups.add(group)
            form.instance.user = user
            form.instance.slug_empresa = slugify(
                form.instance.nombre_empresa+"-"+str(user.pk),
                allow_unicode=True)
            form.save()
            login(self.request, user)
            return self.get_success_url()
        except Exception as e:
            user.delete()
            raise e


class EmpresaHomepageView(DetailView):
    template_name = "market/empresa_homepage.html"
    model = models.Administrador
    lookup_field = "slug_empresa"
    lookup_url_kwarg = "slug_empresa"
    context_object_name = "administrador"


class CrearDiseñoView(CreateView):
    template_name = "market/form.html"
    form_class = forms.CreateDiseñoForm

    def get_success_url(self):
        return reverse_lazy(
            'market:homepage',
            kwargs={"slug_empresa": "%s" %
                    self.request.user.administrador.slug_empresa})

    def form_valid(self, form):
        proyecto = models.Proyecto.objects.get(pk=self.kwargs["proyecto_id"])
        try:
            form.instance.proyecto = proyecto
            form.instance.estado = models.Diseño.EN_PROCESO
            return super(CrearDiseñoView, self).form_valid(form)
        except Exception as e:
            raise e


# Create your views here.
