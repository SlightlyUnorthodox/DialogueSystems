from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import User, Candidate, Recruiter

#SignIn, general, should we have a register form?
class SignInForm(forms.Form):
	username = forms.CharField(label = 'Username', min_length = 8, max_length = 50, required = True)
	password = forms.CharField(label = 'Password', min_length = 8, widget = forms.PasswordInput(), required = True)

#Candidate information, specific
class CandidateInformation(forms.Form):
	firstName = forms.CharField(label = 'FirstName', min_length = 1, max_length = 100, required = True)
	lastName = forms.CharField(label = 'LastName', min_length = 1, max_length = 100, required = True)
	highestEducation = forms.CharField(label = 'HighestEducation', min_length = 1, max_length = 1, required = True)
	educationStatus = forms.CharField(label = 'EducationStatus', min_length = 1, max_length = 1, required = True)
	programField = forms.CharField(label = 'MajorField', min_length = 1, max_length = 50, required = True)
	yearsExperience = forms.IntegerField(label = 'YearsExperience', min_value = 1, max_value = 20, required = True)
	relevantEmployer = forms.CharField(label = 'RelevantEmployer', min_length = 1, max_length = 50, required = True)
