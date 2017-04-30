from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import admin_views


urlpatterns = [
    #url(r'^$', admin_views.PortalView.as_view(), name='index'),
    url(r'^proyectos/$', 
        login_required(admin_views.ProyectoListView.as_view()), name='proyectos'),
    url(r'^proyectos/nuevo$', 
        login_required(admin_views.CreateProyectoView.as_view()), name='nuevo_proyecto'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/$',
        admin_views.DiseñoListView.as_view(), name='diseños'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/borrar/$',
        admin_views.DeleteProyectoView.as_view(), name='borrar_proyecto'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/editar/$',
        admin_views.UpdateProyectoView.as_view(), name='editar_proyecto'),
    url('^logout/$', auth_views.logout, {}, name='logout'),
    url('^login/$', auth_views.login, {}, name='login'),
]
