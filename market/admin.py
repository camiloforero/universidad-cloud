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



# Register your models here.
