from vanilla import ListView, CreateView, UpdateView, DeleteView
from .models import Diseño, Proyecto
from django.urls import reverse_lazy


class DiseñoListView(ListView):
    model = Diseño
    template_name = "market/lista_diseños.html"

    def get_queryset(self):
        return Diseño.objects.disponibles().filter(
            proyecto_id=self.kwargs["proyecto_id"],
            proyecto__autor_id=self.request.user.administrador)

    def get_context_data(self, **kwargs):
        context = super(DiseñoListView, self).get_context_data(**kwargs)
        context["proyecto"] = self.kwargs["proyecto_id"]
        return context

class ProyectoListView(ListView):
    model = Proyecto
    template_name = "market/lista_proyectos.html"

    def get_queryset(self):
        return Proyecto.objects.filter(
            autor_id=self.request.user.administrador)

    def get_context_data(self, **kwargs):
        context = super(ProyectoListView, self).get_context_data(**kwargs)
        #context["proyecto"] = self.kwargs["id_proyecto"]
        return context

class CreateProyectoView(CreateView):
    model = Proyecto
    template_name = "market/form.html"
    fields = ['nombre', 'descripción', 'valor_estimado']
    success_url = reverse_lazy("portal:proyectos")
    def form_valid(self, form):
        form.instance.autor = self.request.user.administrador
        return super(CreateProyectoView, self).form_valid(form)


class UpdateProyectoView(UpdateView):
    model = Proyecto
    template_name = "market/form.html"
    fields = ['nombre', 'descripción', 'valor_estimado']
    success_url = reverse_lazy("portal:proyectos")
    lookup_url_kwarg = "proyecto_id"


class DeleteProyectoView(DeleteView):
    model = Proyecto
    success_url = reverse_lazy("portal:proyectos")
    lookup_url_kwarg = "proyecto_id"
    template_name = "market/borrar.html"
