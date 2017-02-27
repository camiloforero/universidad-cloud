from django.conf.urls import url
from django.contrib import admin
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
                r'^lista_diseños/$', admin_views.DiseñoList.as_view(),
                name="listaDiseños")
        ]
        return urls + my_urls


admin_site = DesignMatchAdminSite(name="design_match_admin")


@admin.register(models.Proyecto, site=admin_site)
class DiseñoAdmin(admin.ModelAdmin):
    fields = ('nombre', 'descripción', 'valor_estimado')


# Register your models here.
