from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^index', views.index, name = 'index'),
	url(r'^candidate_form', views.candidate_form, name = 'candidate_form'),
	url(r'^interview_page', views.interview_page, name = 'interview_page'),
	url(r'^feedback_page', views.feedback_page, name = 'feedback_page'),
]