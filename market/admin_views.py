from vanilla import ListView
from .models import Diseño


class DiseñoList(ListView):
    model = Diseño
    template_name = "market/admin/diseño/lista_diseños.html"
