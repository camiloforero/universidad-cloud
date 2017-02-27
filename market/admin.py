from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

from . import models, admin_views


class DesignMatchAdminSite(admin.AdminSite):
    site_header = "DesignMatch - Bienvenido"
    site_title = "DesignMatch"
    index_title = "Administrador de diseños"
    index_template = "market/admin/admin_index.html"

    def get_urls(self):
        urls = super(DesignMatchAdminSite, self).get_urls()
        my_urls = [
            url(
                r'^(?P<id_proyecto>\w+)/lista_diseños/$',
                admin_views.DiseñoList.as_view(),
                name="listaDiseños")
        ]
        return urls + my_urls

    def each_context(self, request):
        dict = super(DesignMatchAdminSite, self).each_context(request)
        try:
            dict["site_url"] = reverse_lazy(
                'market:homepage',
                kwargs={"slug_empresa": "%s" %
	    	        request.user.administrador.slug_empresa})
        except:
            pass
        return dict


admin_site = DesignMatchAdminSite(name="design_match_admin")


@admin.register(models.Proyecto, site=admin_site)
class ProyectoAdmin(admin.ModelAdmin):
    fields = ('nombre', 'descripción', 'valor_estimado')
    readonly_fields = ('num_diseños', 'ver_diseños')
    list_display = ('__str__', 'valor_estimado', 'num_diseños', 'ver_diseños')

    def num_diseños(self, instance):
        cantidad = instance.diseños.count()
        return cantidad
    num_diseños.short_description = "Número de diseños"

    def ver_diseños(self, instance):
        return mark_safe(
            '<a href="%s">Ver todos los diseños</a>' %
            reverse_lazy(
                'design_match_admin:listaDiseños',
                kwargs={'id_proyecto': "%s" % instance.pk}))

    ver_diseños.short_description = "Ver todos los diseños"

    def get_queryset(self, request):
        qs = super(ProyectoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user.administrador)

    def save_model(self, request, obj, form, change):
        obj.autor = request.user.administrador
        super(ProyectoAdmin, self).save_model(request, obj, form, change)


admin_site.register(Group)

# Register your models here.
