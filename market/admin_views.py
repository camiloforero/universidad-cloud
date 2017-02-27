from vanilla import ListView
from .models import Diseño


class DiseñoList(ListView):
    model = Diseño
    template_name = "market/admin/diseño/lista_diseños.html"
    #TODO: Forma para que muestre sólo los diseños del proyecto en específico al cual pertenece la url
