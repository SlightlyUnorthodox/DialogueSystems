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
from django.utils import dateformat

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
	start_time = datetime.datetime.now()
	start_time = start_time.strftime("%Y-%m-%d %H:%M")

	newInterview = Interview(
		candidate = candidate,
		recruiter = newRecruiter,
		start_time = start_time,
		end_time = start_time)
	newInterview.save()

	# Set interview id global
	global interview_id
	interview_id = newInterview.interview_id

	return(interview_id)
##
##
##

#
# 1. Candidate Form - enter generic information for use in interview
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
			newDemoCandidate = Candidate(
				user = newDemoUser,
				first_name = newFirstName,
				last_name = newLastName,
				highest_education = newHighestEd,
				education_status = newEducationStatus,
				program = newProgram,
				years_experience = newYearsExperience,
				relevant_job_employer = newRelevantEmployer,
				relevant_job_title = newRelevantJobTitle)

			newDemoCandidate.save()

			# Save candidate as global candidate
			global candidate_id
			candidate_id = newDemoCandidate.candidate_id

			# Confirm successfuly creation of new user
			print("Log: new candidate successfully created")
			state = "Application submitted. Proceed to next page."

			# Initialize interview
			initialize_interview(newDemoUser, newDemoCandidate)
			print("GLOBAL INTERVIEW ID: " + str(interview_id))

			# Redirect user to next page
			return HttpResponseRedirect('/pre_survey/')
	else:
		# Initialize candidate form
		form = CandidateForm()

	# Cycle initialized form
	state = "Please enter candidate information"
	return render(request, 'candidate_form.html', {'form':form, 'state':state})

# 2. Pre Survey - pre-dialogue user satisfaction/outlook survey
def pre_survey(request):
	# Initialize candidate model variables
	questionOneResponse = questionTwoResponse = questionThreeResponse = questionFourResponse = questionFiveResponse = ''

	# Check if POST request was made
	if request.method == 'POST':
		# Validate candidate form
		form = PreSurveyForm(request.POST)
		if form.is_valid():

			# Get interview instance
			print("Checking interview_id: " + str(interview_id))

			current_interview_obj = Interview.objects.get(interview_id = int(interview_id))

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
				interview = current_interview_obj,
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

			return HttpResponseRedirect('/interview_page/')
			#return render(request, 'interview_page.html', {'form':form, 'state':state, 'interview': request.session.get('interview', None)})
	else:
		# Initialize candidate form
		form = PostSurveyForm()

	# Cycle initialized form
	state = "Please enter pre-screening survey information"
	return render(request, 'pre_survey.html', {'form':form, 'state':state})

# 3. Interview Page - hosts dialogue for interview
def interview_page(request):

	# Confirm candidate and interview info forwarding
	candidate = Candidate.objects.get(candidate_id = int(candidate_id))
	interview = Interview.objects.get(interview_id = int(interview_id))

	print(candidate.first_name)
	print(candidate.last_name)
	print(candidate.highest_education)

	print(interview.start_time)
	print(interview.end_time)

	return render(request, 'interview_page.html', {'interview':request.session.get('interview', None)})

# 4. Feedback Page - provides dialogue feedback for candidate and recruiter
def feedback_page(request):
	
	return render(request, 'feedback_page.html', {'interview':request.session.get('interview', None)})

# 5. Post Survey - post-dialogue user satisfaction survey
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



