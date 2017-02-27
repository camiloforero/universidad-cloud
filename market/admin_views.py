from vanilla import ListView
from .models import Diseño


class DiseñoList(ListView):
    model = Diseño
    template_name = "market/admin/diseño/lista_diseños.html"

    def get_queryset(self):
        return Diseño.objects.filter(
            proyecto_id=self.kwargs["id_proyecto"],
            proyecto__autor_id=self.request.user.administrador)

    def get_context_data(self, **kwargs):
        context = super(DiseñoList, self).get_context_data(**kwargs)
        context["proyecto"] = self.kwargs["id_proyecto"]
        return context
    #TODO: Forma para que muestre sólo los diseños del proyecto en específico al cual pertenece la url
