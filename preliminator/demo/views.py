from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from .models import Candidate, Interview

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def candidate_form(request):
	template = loader.get_template('candidate_form.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def interview_page(request):
	template = loader.get_template('interview_page.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def feedback_page(request):
	template = loader.get_template('feedback_page.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))