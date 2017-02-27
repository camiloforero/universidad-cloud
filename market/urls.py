from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^registro/$', views.RegistroView.as_view(), name='registro'),
    url(r'^(?P<slug_empresa>[\w-]+)/$',
        views.EmpresaHomepageView.as_view(), name='homepage'),
    url(r'^(?P<id_proyecto>\d+)/nuevo_diseño/$',
        views.CrearDiseñoView.as_view(), name='nuevo_diseño')
]
