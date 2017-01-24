from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.dialogue, name = 'dialogue'),
	url(r'^.*/$', views.dialogue, name = 'dialogue'),
	url(r'^process_ajax', views.process_ajax, name='process_ajax'),
]
