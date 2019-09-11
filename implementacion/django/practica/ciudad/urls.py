from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.HomePageView.as_view(), name = 'home'),
	url(r'^trafico_data/$', views.trafico_datasets, name = 'trafico'),
	url(r'^update_disponible/$', views.update_disponible, name = 'updatedisponible'),
	url(r'^trafico_modelo/(?P<modelo>\w{0,50})/$', views.trafico_modelo, name = 'traficomodelo'),
	url(r'^disponible_data_tipo/(?P<tipo>\w{0,50})/$', views.disponible_datasets_tipo, name = 'disponibletipo'),
]
