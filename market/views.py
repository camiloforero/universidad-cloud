from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.urls import reverse_lazy
from . import forms, models

from vanilla import TemplateView, FormView


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


# Create your views here.
