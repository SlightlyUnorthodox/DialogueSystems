#Dax Gerts, Sara Lichtenstein, Forms
from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import User, Candidate, Recruiter, Interview, Transcript	

#SignIn, general, should we have a register form?
class SignInForm(forms.Form):
	username = forms.CharField(label = 'Username', min_length = 8, max_length = 50, required = True)
	password = forms.CharField(label = 'Password', min_length = 8, widget = forms.PasswordInput(), required = True)

#Candidate information, specific
class CandidateForm(forms.Form):
	firstName = forms.CharField(label = 'First Name', min_length = 1, max_length = 100, required = True)
	lastName = forms.CharField(label = 'Last Name', min_length = 1, max_length = 100, required = True)
	
	# Education levels
	EDU_LEVELS = (
		('N', 'None'),
		('H', 'High School Diploma'),
		('T', 'Technical Diploma'),
		('A', 'Associate\'s Degree'),
		('B', 'Bachelor\'s Degree'),
		('M', 'Master\'s Degree'),
		('D', 'Doctorate Degree')
	)

	highestEducation = forms.ChoiceField(choices = EDU_LEVELS, label = 'Highest Education Level', required = True, initial =  'B')
	
	# Education status levels
	EDU_STATUS = (
		('G', 'Graduated'),
		('I', 'In Progress'),
		('N', 'Not Complete'),
		('X', 'NA')
	)

	educationStatus = forms.ChoiceField(choices = EDU_STATUS, label = 'Education Status', required = True, initial =  'I')

	programField = forms.CharField(label = 'Major/Field', min_length = 1, max_length = 50, required = False)
	yearsExperience = forms.IntegerField(label = 'Years of Experience In Field (Academics Included)', min_value = 1, max_value = 80, required = True)
	relevantEmployer = forms.CharField(label = 'Relevant Employer', min_length = 1, max_length = 50, required = False)
	relevantTitle = forms.CharField(label = 'Relevant Job Title', min_length = 1, required = False)

#Recruiter information
class RecruiterForm(forms.Form):
	firstName = forms.CharField(label = 'First Name', min_length = 1, max_length = 100, required = True)
	lastName = forms.CharField(label = 'Last Name', min_length = 1, max_length = 100, required = True)
	employer = forms.CharField(label = 'Employer', min_length = 1, max_length = 50, required = True)
	title = forms.CharField(label = 'Title', min_length = 1, max_length = 50, required = True)

#PreSurvey
class PreSurveyForm(forms.Form):

	# Predefine possible response in pre-survey
	RESPONSES = (
		(1, 'Strongly disagree'),
		(2, 'Disagree'),
		(3, 'Neutral'),
		(4, 'Agree'),
		(5, 'Strongly Agree')
	)

	questionOneResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 1: I am interested in using dialogue systems to help me with tasks.', required = True, initial =  3)
	questionTwoResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 2: I believe this system will help prepare me for interviews.', required = True, initial =  3)
	questionThreeResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 3: I am confident this system will understand me majority of the time.', required = True, initial =  3)
	questionFourResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 4: I believe this system will be easy to use.', required = True, initial =  3)
	questionFiveResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 5: I have previous experience using dialogue systems.', required = True, initial =  3)

#PostSurvey
class PostSurveyForm(forms.Form):

	# Predefine possible response in pre-survey
	RESPONSES = (
		(1, 'Strongly disagree'),
		(2, 'Disagree'),
		(3, 'Neutral'),
		(4, 'Agree'),
		(5, 'Strongly Agree')
	)

	questionOneResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 1: This system has sustained or fostered my interest in using dialogue systems to help me with tasks.', required = True, initial =  3)
	questionTwoResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 2: I believe this system has helped prepare me for interviews.', required = True, initial =  3)
	questionThreeResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 3: I am confident this system understood me majority of the time.',required = True, initial =  3)
	questionFourResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 4: This system was easy to use.', required = True, initial =  3)
	questionFiveResponse = forms.ChoiceField(choices = RESPONSES, label = 'Question 5: I believe my previous experience helped me use this dialogue system.', required = True, initial =  3)

#Transcript
class TranscriptForm(forms.Form):
	speakerChoice = forms.CharField(label = 'Speaker', max_length = 1, required = True)
	lineNumber = forms.IntegerField(label = 'Line Number', min_value = 1, max_value = 2000)
	lineContents = forms.CharField(label = 'Line Content', min_length = 1, max_length = 2000)

#Interview Post Form
class PostForm(forms.ModelForm):
	class Meta:
		model = Transcript	
		fields = ['line_contents']
		widgets = {
			'line_contents': forms.TextInput(
				attrs={'id': 'inputText', 'required': True, 'placeholder': 'nah'}
				),
		}