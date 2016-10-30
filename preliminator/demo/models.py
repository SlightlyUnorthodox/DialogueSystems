from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator

##
## System user information
##

# Table for system users
class User(models.Model):
	# Key field def
	user_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.user_id

	# Generic username requirements
	username = models.CharField(
		"Username",
		max_length = 50, 
		validators = [MinLengthValidator(8, "Your username must contain at least 8 characters.")]#,
		#unique = True
		)
	def __unicode__(self):
		return self.username

	# Generic password requirements
	password = models.CharField(
		"Password",
		max_length = 50,
		validators = [MinLengthValidator(8, "Your username must contain at least 8 characters.")]
		)
	def __unicode__(self):
		return self.password

	# Allow many-to-one relation between user and (candidate/recruiter)
	pass

	
# Job candidates/applicants information
class Candidate(models.Model):
	# Key field def
	candidate_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.candidate_id
	
	# One-to-one relationship with user
	user = models.ForeignKey(
		User,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.user
	
	# Candidate first name
	first_name = models.CharField(
		"First name",
		max_length = 50,
		validators = [RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters allowed')]
	)
	def __unicode__(self):
		return self.first_name

	# Candidate last name
	last_name = models.CharField(
		"Last name",
		max_length = 50,
		validators = [RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters allowed')]
	)
	def __unicode__(self):
		return self.last_name

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

	# Candidate's highest education level
	highest_education = models.CharField(
		max_length = 1,
		choices = EDU_LEVELS
	)
	def __unicode__(self):
		return self.highest_education

	# Education status levels
	EDU_STATUS = (
		('G', 'Graduated'),
		('I', 'In Progress'),
		('N', 'Not Complete')
	)

	# Candidate's education status
	education_status = models.CharField(
		max_length = 1,
		choices = EDU_STATUS
	)
	def __unicode__(self):
		return self.education_status

	# Program (major/field)
	program = models.CharField(
		max_length = 50,
		validators = [RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters allowed')]
	)
	def __unicode__(self):
		return self.program

	# Years experience (in Industry)
	years_experience = models.PositiveIntegerField()
	def __unicode__(self):
		return self.years_experience
	
	#
	# The following pertain to a most recent, relevant job
	#

	# Most relevant job employer
	relevant_job_employer = models.CharField(
		max_length = 50
	)
	def __unicode__(self):
		return self.recent_employer

	# Most relevant job title
	relevant_job_title = models.CharField(
		max_length = 50
	)

	# Allow many-to-one relation between candidate and interview
	pass

# Job recruiter information
class Recruiter(models.Model):
	# Key field def
	recruiter_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.recruiter_id
	
	# One-to-one relationship with user
	user = models.ForeignKey(
		User,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.user
	
	# Candidate first name
	first_name = models.CharField(
		max_length = 50,
		validators = [RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters allowed')]
	)
	def __unicode__(self):
		return self.first_name

	# Candidate last name
	last_name = models.CharField(
		max_length = 50,
		validators = [RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters allowed')]
	)
	def __unicode__(self):
		return self.last_name

	# Recruiter's employer/company
	employer = models.CharField(
		max_length = 50,
		validators = [RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters allowed')]
	)
	def __unicode__(self):
		return self.employer

	# Recruiter's title
	title = models.CharField(
		max_length = 50,
		validators = [RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters allowed')]
	)
	def __unicode__(self):
		return self.title


	# Allow many-to-one relation between recruiter and interview
	pass

##
## Primary log for interview output/decisions
##

# Interview metadata
class Interview(models.Model):
	# Key field def
	interview_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.interview_id

	# Interview candidate
	candidate = models.ForeignKey(
		Candidate,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.candidate
	
	# Interview recruiter
	recruiter = models.ForeignKey(
		Recruiter,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.recruiter
	
	# Interview start time
	start_time = models.DateTimeField()
	def __unicode__(self):
		return self.start_time

	# Interview end time
	end_time = models.DateTimeField()
	def __unicode__(self):
		return self.end_time

	# Allow many-to-one relation between intervie and surveys/transcript/feedback
	pass

##
## Interview sub-tables
##

# Pre-interview survey
class PreSurvey(models.Model):
	# Key field def
	presurvey_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.presurvey_id

	# One-to-one relationship with interview
	interview = models.ForeignKey(
		Interview,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.interview

	# Predefine possible response in pre-survey
	RESPONSES = (
		(1, 'Strongly disagree'),
		(2, 'Disagree'),
		(3, 'Neutral'),
		(4, 'Agree'),
		(5, 'Strongly Agree')
	)

	# Question 1
	question_one_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_one_response

	# Question 2
	question_two_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_two_response

	# Question 3
	question_three_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_three_response

	# Question 4
	question_four_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_four_response

	# Question 5
	question_five_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_five_response

# Post-interview survey
class PostSurvey(models.Model):
	# Key field def
	postsurvey_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.postsurvey_id

	# One-to-one relationship with interview
	interview = models.ForeignKey(
		Interview,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.interview

	# Predefine possible response in post-survey
	RESPONSES = (
		(1, 'Strongly disagree'),
		(2, 'Disagree'),
		(3, 'Neutral'),
		(4, 'Agree'),
		(5, 'Strongly Agree')
	)

	# Question 1
	question_one_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_one_response

	# Question 2
	question_two_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_two_response

	# Question 3
	question_three_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_three_response

	# Question 4
	question_four_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_four_response

	# Question 5
	question_five_response = models.CharField(
		max_length = 1,
		choices = RESPONSES
	)
	def __unicode__(self):
		return self.question_five_response


# Interview/screening transcripts
class Transcript(models.Model):
	# Key field def
	transcript_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.transcript_id

	# One-to-one relationship with interview
	interview = models.ForeignKey(
		Interview,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.interview	

	# Possible speakers
	SPEAKERS = (
		('C', 'Candidate'),
		('R', 'Recruiter')
	)

	# Speaker
	speaker = models.CharField(
		max_length = 1,
		choices = SPEAKERS
	)
	def __unicode__(self):
		return self.speaker

	# Line number (utterance number)
	line_number = models.PositiveIntegerField()
	def __unicode__(self):
		return self.line_number

	# Line contents (words spoken in utterance)
	line_contents = models.CharField(
		max_length = 2000
	)
	def __unicode__(self):
		return self.line_contents

# Interview feedback fields
class Feedback(models.Model):
	# Key field def
	feedback_id = models.AutoField(primary_key = True)
	def __unicode__(self):
		return self.feedback_id

	# One-to-one relationship with interview
	interview = models.ForeignKey(
		Interview,
		on_delete = models.CASCADE
	)
	def __unicode__(self):
		return self.interview

	# Define possible feedback targets
	FEEDBACK_TARGETS = (
		('R', 'Recruiter'),
		('C', 'Candidate'),
		('S', 'System')
	)

	# The target to which the feedback text is displayed/sent
	feedback_target = models.CharField(
		max_length=1, 
		choices = FEEDBACK_TARGETS
	)
	def __unicode__(self):
		return self.feedback_target

	# Human-readable text of interview feedback
	feedback_contents = models.CharField(
		max_length = 500, # Arbitrary, subject to reevaluation
		)
	def __unicode__(self):
		return self.feedback_contents
