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
		validators = [MinLengthValidator(8, "Your username must contain at least 8 characters.")],
		unique = True
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

	##
	## TODO: Fill with remaining fields from candidate form
	##

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