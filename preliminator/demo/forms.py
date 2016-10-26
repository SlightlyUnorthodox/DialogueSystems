from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import User, Candidate, Recruiter

#SignIn, general, should we have a register form?
class SignInForm(forms.Form):
	username = forms.CharField(label = 'Username', min_length = 8, max_length = 50, required = True)
	password = forms.CharField(label = 'Password', min_length = 8, widget = forms.PasswordInput(), required = True)

#Candidate information, specific
class CandidateForm(forms.Form):
	firstName = forms.CharField(label = 'FirstName', min_length = 1, max_length = 100, required = True)
	lastName = forms.CharField(label = 'LastName', min_length = 1, max_length = 100, required = True)
	highestEducation = forms.CharField(label = 'HighestEducation', max_length = 1, required = True)
	educationStatus = forms.CharField(label = 'EducationStatus', max_length = 1, required = True)
	programField = forms.CharField(label = 'MajorField', min_length = 1, max_length = 50, required = True)
	yearsExperience = forms.IntegerField(label = 'YearsExperience', min_value = 1, max_value = 20, required = True)
	relevantEmployer = forms.CharField(label = 'RelevantEmployer', min_length = 1, max_length = 50, required = True)

#Recruiter information
class RecruiterForm(forms.Form):
	firstName = forms.CharField(label = 'FirstName', min_length = 1, max_length = 100, required = True)
	lastName = forms.CharField(label = 'LastName', min_length = 1, max_length = 100, required = True)
	employer = forms.CharField(label = 'Employer', min_length = 1, max_length = 50, required = True)
	title = forms.CharField(label = 'Title', min_length = 1, max_length = 50, required = True)

#PreSurvey
class PreSurveyForm(forms.Form):
	questionOneResponse = forms.CharField(label = 'QuestionOneResponse', max_length = 1, required = True)
	questionTwoResponse = forms.CharField(label = 'QuestionTwoResponse', max_length = 1, required = True)
	questionThreeResponse = forms.CharField(label = 'QuestionThreeResponse', max_length = 1, required = True)
	questionFourResponse = forms.CharField(label = 'QuestionFourResponse', max_length = 1, required = True)
	questionFiveResponse = forms.CharField(label = 'QuestionFiveResponse', max_length = 1, required = True)

#PostSurvey
class PostSurveyForm(forms.Form):
	questionOneResponse = forms.CharField(label = 'QuestionOneResponse', max_length = 1, required = True)
	questionTwoResponse = forms.CharField(label = 'QuestionTwoResponse', max_length = 1, required = True)
	questionThreeResponse = forms.CharField(label = 'QuestionThreeResponse', max_length = 1, required = True)
	questionFourResponse = forms.CharField(label = 'QuestionFourResponse', max_length = 1, required = True)
	questionFiveResponse = forms.CharField(label = 'QuestionFiveResponse', max_length = 1, required = True)

#Transcript
class TranscriptForm(forms.Form):
	speakerChoice = forms.CharField(label = 'Speaker', max_length = 1, required = True)
	lineNumber = forms.IntegerField(label = 'LineNumber', min_value = 1, max_value = 2000)
	lineContents = forms.CharField(label = 'LineContent', min_length = 1, max_length = 2000)
