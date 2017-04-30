from vanilla import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.urls import reverse_lazy
from django.conf import settings
from boto3.dynamodb.conditions import Key, Attr
from .forms import CreateProyectoForm


class DiseñoListView(TemplateView):
    template_name = "market/lista_diseños.html"

    def get_context_data(self, **kwargs):
        diseños_table = settings.DYNAMODB_ENDPOINT.Table('disenhos')        
        slug = self.kwargs["slug_empresa"]
        context = super(DiseñoListView, self).get_context_data(**kwargs)
        diseños = diseños_table.query(
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('id_diseño').eq(
                '%s###%s' % (slug, self.kwargs['nombre_proyecto']))
            )['Items']
        context["diseños"] = diseños
        return context

class ProyectoListView(TemplateView):
    template_name = "market/lista_proyectos.html"

    def get_context_data(self, **kwargs):
        empresas = settings.TABLA_EMPRESAS
        proyectos_table = settings.DYNAMODB_ENDPOINT.Table('proyectos')
        context = super(ProyectoListView, self).get_context_data(**kwargs)
        empresa_query = empresas.query(
            IndexName='id_usuario-index',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('id_usuario').eq(self.request.user.id)
        )
        empresa = empresa_query['Items'][0]
        proyectos = proyectos_table.query(
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('slug_empresa').eq(empresa['slug_empresa'])
        )
        context['proyecto_list'] = proyectos['Items']
        context['slug_empresa'] = empresa['slug_empresa']
        #context["proyecto"] = self.kwargs["id_proyecto"]
        return context

class CreateProyectoView(FormView):
    template_name = "market/form.html"
    form_class = CreateProyectoForm
    success_url = reverse_lazy("portal:proyectos")
    def form_valid(self, form):
        empresas = settings.DYNAMODB_ENDPOINT.Table('empresas')
        proyectos_table = settings.DYNAMODB_ENDPOINT.Table('proyectos')
        empresa_query = empresas.query(
            IndexName='id_usuario-index',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('id_usuario').eq(self.request.user.id)
        )
        empresa = empresa_query['Items'][0]
        proyecto_data = {
            'slug_empresa': empresa['slug_empresa'],
            'nombre': form.cleaned_data['nombre'],
            'descripción': form.cleaned_data['descripción'],
            'valor_estimado': form.cleaned_data['valor_estimado'],
            'diseños': []
        }

        proyectos_table.put_item(
            Item=proyecto_data,
            ConditionExpression=Attr('slug_empresa').not_exists()|Attr('nombre').not_exists()
        )

        return super(CreateProyectoView, self).form_valid(form)


class UpdateProyectoView(UpdateView):
    template_name = "market/form.html"
    fields = ['nombre', 'descripción', 'valor_estimado']
    success_url = reverse_lazy("portal:proyectos")
    lookup_url_kwarg = "proyecto_id"


class DeleteProyectoView(DeleteView):
    success_url = reverse_lazy("portal:proyectos")
    lookup_url_kwarg = "proyecto_id"
    template_name = "market/borrar.html"
