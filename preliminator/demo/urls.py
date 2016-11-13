from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^index', views.index, name = 'index'),
	url(r'^candidate_form', views.candidate_form, name = 'candidate_form'),
	url(r'^pre_survey', views.pre_survey, name = 'pre_survey'),
	url(r'^interview_page', views.interview_page, name = 'interview_page'),
	url(r'^feedback_page', views.feedback_page, name = 'feedback_page'),
	url(r'^post_survey', views.post_survey, name = 'post_survey'),
	url(r'^process_ajax', views.process_ajax, name='process_ajax'),
	url(r'^', views.index, name = 'index'),

]

# urlpatterns = [
# 	url(r'^$', views.index, name = 'index'),
# 	url(r'^index', views.index, name = 'index'),
# 	url(r'^candidate_form', views.candidate_form, name = 'candidate_form'),
# 	url(r'^pre_survey/(?P<interview_id>\d+)/$', views.pre_survey, name = 'pre_survey'),
# 	url(r'^interview_page/(?P<interview_id>\d+)/$', views.interview_page, name = 'interview_page'),
# 	url(r'^feedback_page/(?P<interview_id>\d+)/$', views.feedback_page, name = 'feedback_page'),
# 	url(r'^post_survey/(?P<interview_id>\d+)/$', views.post_survey, name = 'post_survey'),
# 	url(r'^', views.index, name = 'index')
# ]
