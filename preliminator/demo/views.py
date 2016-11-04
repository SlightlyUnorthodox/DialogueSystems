from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import *
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.core.mail import EmailMessage

import datetime
import decimal

#import necessary models and forms
from .models import Candidate, Interview, User, Recruiter, PreSurvey, PostSurvey, Transcript, Feedback
from .forms import CandidateForm, PreSurveyForm, PostSurveyForm

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

##
## CRITICAL COMPONENT - DO NOT TOUCH LIGHTLY
##

def initialize_interview(user, candidate):

	# Create demo recruiter
	newRecruiter = Recruiter(
		user = user,
		first_name = "John",
		last_name = "Smith",
		employer = "Company A",
		title = "Hiring Manager")
	newRecruiter.save()

	# Initialize Interview
	newInterview = Interview(
		candidate = candidate,
		recruiter = newRecruiter,
		start_time = datetime.datetime.now())
	newInterview.save()

	return(newInterview)

##
##
##

@csrf_exempt
def candidate_form(request):
	# Initialize candidate model variables
	newFirstName = newLastName = newHighestEducation = newEducationStatus = newProgramField = newYearsExperience = newRelevantEmployer = ''

	# Check if POST request was made
	if request.method == 'POST':

		# Validate candidate form
		form = CandidateForm(request.POST)
		if form.is_valid():

			# Handle form input

			# First name
			newFirstName = request.POST.get('firstName')

			# Last name
			newLastName = request.POST.get('lastName')

			# Highest education
			newHighestEd = request.POST.get('highestEducation')

			# Education status
			newEducationStatus = request.POST.get('educationStatus')

			# Program field
			newProgram = request.POST.get('programField')

			# Years experience
			newYearsExperience = request.POST.get('yearsExperience')
			
			# Relevant employer
			newRelevantEmployer = request.POST.get('relevantEmployer')

			# Relevant job title
			newRelevantJobTitle = request.POST.get('relevantTitle')

			##
			## ADD TEMPFIX FOR USER DEPENDENCY
			##

			# New User 
			newDemoUser = User(
				username = "demo_user",
				password = "demo_password"
			)
			newDemoUser.save()

			# Save new candidate
			newCandidate = Candidate(
				user = newDemoUser,
				first_name = newFirstName,
				last_name = newLastName,
				highest_education = newHighestEd,
				education_status = newEducationStatus,
				program = newProgram,
				years_experience = newYearsExperience,
				relevant_job_employer = newRelevantEmployer,
				relevant_job_title = newRelevantJobTitle)

			newCandidate.save()

			# Confirm successfuly creation of new user
			print("Log: new candidate successfully created")
			state = "Application submitted. Proceed to next page."

			# Initialize interview
			interview =	initialize_interview(newDemoUser, newDemoCandidate)
			print(interview)
			print(interview.interview_id)
			# Redirect user to next page
			return render(request, 'interview_page.html', {'form':form, 'state':state})

			# TODO: Confirm if using pre-survey
			# return render(request, 'pre_survey.html', {'form': form, 'state': state, 'interview': interview})
	else:
		# Initialize candidate form
		form = CandidateForm()

	# Cycle initialized form
	state = "Please enter candidate information"
	return render(request, 'candidate_form.html', {'form':form, 'state':state})

def interview_page(request):

	return render(request, 'interview_page.html')

def feedback_page(request):
	
	print (request['interview'])
	#request['feedback'] = Feedback.objects.get(interview = request['interview'])
	#template = loader.get_template('feedback_page.html')

	return render(request, 'feedback_page.html')


@csrf_exempt
def pre_survey(request):
	# Initialize candidate model variables
	questionOneResponse = questionTwoResponse = questionThreeResponse = questionFourResponse = questionFiveResponse = ''

	# Check if POST request was made
	if request.method == 'POST':

		# Validate candidate form
		form = PreSurveyForm(request.POST)
		if form.is_valid():

			# Handle form input

			# Question 1
			questionOneResponse = request.POST.get('questionOneResponse')

			# Question 2
			questionTwoResponse = request.POST.get('questionTwoResponse')

			# Question 3
			questionThreeResponse = request.POST.get('questionThreeResponse')

			# Question 4
			questionFourResponse = request.POST.get('questionFourResponse')

			# Question 5
			questionFiveResponse = request.POST.get('questionFiveResponse')

			# Save new candidate
			newPreSurvey = PreSurvey(
				interview = interview,
				question_one_response = questionOneResponse,
				question_two_response = questionTwoResponse,
				question_three_response = questionThreeResponse,
				question_four_response = questionFourResponse,
				question_five_response = questionFiveResponse
			)

			newPreSurvey.save()

			# Confirm successfuly creation of new user
			print("Log: new survey data added to databse.")
			state = "Survey submitted. Proceed to next page."

			# Redirect user to next page
			return render(request, 'candidate_form.html', {'form':form, 'state':state})
	else:
		# Initialize candidate form
		form = PostSurveyForm()

	# Cycle initialized form
	state = "Please enter pre-screening survey information"
	return render(request, 'pre_survey.html', {'form':form, 'state':state})

@csrf_exempt
def post_survey(request):
	# Initialize candidate model variables
	questionOneResponse = questionTwoResponse = questionThreeResponse = questionFourResponse = questionFiveResponse = ''

	# Check if POST request was made
	if request.method == 'POST':

		# Validate candidate form
		form = PostSurveyForm(request.POST)
		if form.is_valid():

			# Handle form input

			# Question 1
			questionOneResponse = request.POST.get('questionOneResponse')

			# Question 2
			questionTwoResponse = request.POST.get('questionTwoResponse')

			# Question 3
			questionThreeResponse = request.POST.get('questionThreeResponse')

			# Question 4
			questionFourResponse = request.POST.get('questionFourResponse')

			# Question 5
			questionFiveResponse = request.POST.get('questionFiveResponse')

			# Save new candidate
			newPostSurvey = PostSurvey(
				interview = interview,
				question_one_response = questionOneResponse,
				question_two_response = questionTwoResponse,
				question_three_response = questionThreeResponse,
				question_four_response = questionFourResponse,
				question_five_response = questionFiveResponse
			)

			newPostSurvey.save()

			# Confirm successfuly creation of new user
			print("Log: new survey data added to databse.")
			state = "Survey submitted. Return to index."

			# Redirect user to next page
			return render(request, 'index.html', {'form':form, 'state':state})
	else:
		# Initialize candidate form
		form = PostSurveyForm()

	# Cycle initialized form
	state = "Please enter post-screening survey information"
	return render(request, 'post_survey.html', {'form':form, 'state':state})



