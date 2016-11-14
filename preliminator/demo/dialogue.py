import nltk
import datetime
import threading
import collections
import random
import re

from .models import Candidate, Interview, User, Recruiter, PreSurvey, PostSurvey, Transcript, Feedback

# TODO: Expand as more patterns are identified
affirmative_patterns = re.compile("(yes)|(mhm)|(uhuh)|(okay)")
negative_patterns = re.compile("(no)")
any_pattern = re.compile(".?")
likert_patterns_one =  re.compile("(one)|1")
likert_patterns_two =  re.compile("(two)|2")
likert_patterns_three =  re.compile("(three)|3")
likert_patterns_four =  re.compile("(four)|4")
likert_patterns_five =  re.compile("(five)|5")
gpa_patterns = re.compile("((zero|one|two|three|four) point( zero| one| two| three| four| five| six| seven| eight| nine){1,2})|([0-4]\.\d{1,2})")

class DialogueManager:
	def __init__(self, candidate_id = 1, interview_id = 1):

		# Dialogue time variables
		self.start_time = datetime.datetime.now()
		self.current_time = datetime.datetime.now()
		self.run_time = 0
		self.max_time = 3 # Max 3 minutes

		# Dialogue information fields
		self.candidate_id = candidate_id
		self.interview_id = interview_id
		self.candidate = Candidate.objects.get(candidate_id = int(candidate_id))
		self.interview = Interview.objects.get(interview_id = int(interview_id))

		# Dialogue state information
		self.dialogue_state = 'greeting'
		self.dialogue_state_act = 0 # Indicates index of 
		self.dialogue_state_utterance = 0
		self.dialogue_phrase = 'utterances'
		self.grounding_active = 0 # If 1, indicates grounding state should be evaluated before continuing
		self.end_state = 'closing'
		self.initiative = 'system'
		self.current_speaker = 'system'
		self.proceed = False
		self.cycle_timeout = 0
		self.validation = False
		# Store recent utterances
		self.current_system_utterance = ""
		self.current_user_utterance = ""
		self.user_response = ""
		self.user_response_value = ""

		# Dialogue feature sets
		self.resume_set = collections.OrderedDict([
			('first_name', [0, 'Candidate']), # 0 - incomplete, 1 - complete
			('last_name', [0, '']),
			('highest_education', [0, 'N']),
			('education_status', [0, 'X']),
			('program', [0, '']),
			('years_experience', [0, 0]),
			('relevant_job_employer', [0, '']),
			('relevant_job_title', [0, '']),
		])

		self.skills_set = collections.OrderedDict([
			('Java', [0, 0]), # 0 - na, 1-5 (strongly disagree to strongly agree)
			('C++', [0, 0]),
			('Databases', [0, 0]),
			('Git', [0, 0]),
			('Networking', [0, 0]),
		])

		self.eligibility_set = collections.OrderedDict([
			('citizen', [0, 0]), # 0 - na, 1 - no, 2 - yes
			('visa', [0, 0]), # 0 - na, 1 - not needed, 2 - needed
			('disability', [0, 0]), # 0 - na, 1 - no, 2 - yes
			('veteran', [0, 0]), # 0 - na, 1 - no, 2 - yes
		])

		# Populate candidate fields
		self.__populate_fields()
		
		# Define dialogue pairs (prompt-response) for each state

		# Greeting state pairs
		self.greeting_acts =  (
			{
				'utterances': ["Hello " + str(self.resume_set['first_name'][1]) + ", my name is Preliminator. We'll be conducting a brief interview today. Ready to begin?",
				"Hello " + str(self.resume_set['first_name'][1]) + ", I'll be conducting a brief screening interview. Ready to begin?"],
				'patterns':{
					"name": any_pattern,
				},
				'grounding':["To end the demo at any time, please speak or enter 'quit'. Thank you."],
				'bad_entry':["No bad entry"]},
		)

		# Resume-driven pairs
		self.resume_acts = (
			{ 
				'utterances': ["I didn't see you enter your GPA, to the best of your knowledge, what is your current GPA?",
				"Would you mind sharing your expected GPA at time of graduation?"],
				'patterns':{
					"gpa": gpa_patterns,
				},
				'grounding':["You entered your GPA as: "],
				'bad_entry':["Please enter GPA as either '#.#' or 'number point number'"]},
		)

		# Job-driven pairs
		self.job_acts = (
			{
				'utterances': ["On a scale of 1 to 5, 'one' being no experience and five 'expert', what level of experience would you say you have with Git?",
				"If you had to rate your experience with Git or Github on a scale of 1 (low) to 5 (high), what would you rate it?"],
				'patterns':{
				 1: likert_patterns_one,
				 2: likert_patterns_two,
				 3: likert_patterns_three,
				 4: likert_patterns_four,
				 5: likert_patterns_five,
				},
				'grounding':["You entered the value: "],
				'bad_entry':["Please enter a value from '1' to '5' or 'one' to 'five'."]},
			{ 
				'utterances': ["On a scale of 1 to 5, 'one' being no experience and five 'expert', what level of experience would you say you have with Java?",
				"If you had to rate your experience with Java on a scale of 1 (low) to 5 (high), what would you rate it?"],
				'patterns':{
				 1: likert_patterns_one,
				 2: likert_patterns_two,
				 3: likert_patterns_three,
				 4: likert_patterns_four,
				 5: likert_patterns_five,
				},
				'grounding':["You entered the value: "],
				'bad_entry':["Please enter a value from '1' to '5' or 'one' to 'five'."]},
		)


		# Eligibility pairs
		self.eligibility_acts = (
			{ 
				'utterances':["Are you a United States citizen?", 
				"Are you eligible for employment in the United States?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':["You entered the value: "],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Will you at any time require visa-sponsorship to continue working?",
				"Do you require visa-sponsorship to work in the US?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':["You entered the value: "],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Are you a United States citizen?", 
				"Are you eligible for employment in the United States?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':["You entered the value: "],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Have you ever been convicted of a felony?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':["You entered the value: "],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Do you require any accomodations in order to complete your work?"
				"Will you need any accomodations to complete the work described?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':["You entered the value: "],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
		)

		# Closing state pairs
		self.closing_acts = (
			{ 
				'utterances':["Well I believe we are out of time. Thank you for taking the time to try the Preliminator demo and have a good day."],
				'patterns':{
				"any": any_pattern,
				},
				'grounding':["This is an example grounding sentence."],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},

		)

		# Dialogue component space information
		self.state_set = collections.OrderedDict([
			('greeting', [0, self.greeting_acts]), # 0 - incomplete, 1 - complete
			('resume', [0, self.resume_acts]),
			('job', [0, self.job_acts]),
			('eligibility', [0, self.eligibility_acts]),
			('closing', [0, self.closing_acts]),
		])

	## Dialogue Manager Utilities

	def __check_timeout(self):
		# If difference in start and current time is greater than max
		#	send signal to cancel process.

		# Renew current time
		self.current_time = datetime.datetime.now()
		self.run_time = self.start_time - self.current_time

		# Check dif
		if(divmod(self.run_time.total_seconds(), 60)[0] > self.max_time):
			# System has surpassed max time
			return(1)

		# System still has time
		return(0)

	def __populate_fields(self):
		# Try and populate all resume fields
		for key in self.resume_set:
			if(self.resume_set[key][0] == 0):
				self.resume_set[key] = [1, getattr(self.candidate, key)]
				self.resume_set[key][0] = 1

	def __update_dialogue_acts(self):

		print(self.user_response_value)

		# Greeting state pairs
		self.greeting_acts =  (
			{
				'utterances': ["Hello " + str(self.resume_set['first_name'][1]) + ", my name is Preliminator. We'll be conducting a brief interview today. Ready to begin?",
				"Hello " + str(self.resume_set['first_name'][1]) + ", I'll be conducting a brief screening interview. Ready to begin?"],
				'patterns':{
					"name": any_pattern,
				},
				'grounding':["To end the demo at any time, please speak or enter 'quit'. Thank you."],
				'bad_entry':["No bad entry"]},
		)

		# Resume-driven pairs
		self.resume_acts = (
			{ 
				'utterances': ["I didn't see you enter your GPA, to the best of your knowledge, what is your current GPA?",
				"Would you mind sharing your expected GPA at time of graduation?"],
				'patterns':{
					"gpa": gpa_patterns,
				},
				'grounding':[str("You entered your GPA as " + str(self.user_response_value) + ", yes?")],
				'bad_entry':["Please enter GPA as either '#.#' or 'number point number'"]},
		)

		# Job-driven pairs
		self.job_acts = (
			{
				'utterances': ["On a scale of 1 to 5, 'one' being no experience and five 'expert', what level of experience would you say you have with Git?",
				"If you had to rate your experience with Git or Github on a scale of 1 (low) to 5 (high), what would you rate it?"],
				'patterns':{
				 1: likert_patterns_one,
				 2: likert_patterns_two,
				 3: likert_patterns_three,
				 4: likert_patterns_four,
				 5: likert_patterns_five,
				},
				'grounding':["You entered the value " + str(self.user_response_value) + ", did you not?"],
				'bad_entry':["Please enter a value from '1' to '5' or 'one' to 'five'."]},
			{ 
				'utterances': ["On a scale of 1 to 5, 'one' being no experience and five 'expert', what level of experience would you say you have with Java?",
				"If you had to rate your experience with Java on a scale of 1 (low) to 5 (high), what would you rate it?"],
				'patterns':{
				 1: likert_patterns_one,
				 2: likert_patterns_two,
				 3: likert_patterns_three,
				 4: likert_patterns_four,
				 5: likert_patterns_five,
				},
				'grounding':["You entered the value " + str(self.user_response_value) + ", did you not?"],
				'bad_entry':["Please enter a value from '1' to '5' or 'one' to 'five'."]},
		)


		# Eligibility pairs
		self.eligibility_acts = (
			{ 
				'utterances':["Are you a United States citizen?", 
				"Are you eligible for employment in the United States?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':[str(self.user_response_value) + "?"],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Will you at any time require visa-sponsorship to continue working?",
				"Do you require visa-sponsorship to work in the US?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':[str(self.user_response_value) + "?"],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Are you a United States citizen?", 
				"Are you eligible for employment in the United States?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':[str(self.user_response_value) + "?"],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Have you ever been convicted of a felony?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':[str(self.user_response_value) + "?"],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
			{ 
				'utterances':["Do you require any accomodations in order to complete your work?"
				"Will you need any accomodations to complete the work described?"],
				'patterns':{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				},
				'grounding':[str(self.user_response_value) + "?"],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},
		)

		# Closing state pairs
		self.closing_acts = (
			{ 
				'utterances':["Well I believe we are out of time. Thank you for taking the time to try the Preliminator demo and have a good day."],
				'patterns':{
				"any": any_pattern,
				},
				'grounding':["This is an example grounding sentence."],
				'bad_entry':["Please enter a value 'yes' or 'no'."]},

		)
	
	def check_state(self):

		# Check to see if current state has remaining utterances ## TODO: make more sophisticated
		if ((self.dialogue_state_act + 1) >= len(self.state_set[self.dialogue_state][1])):
			# If no more utterances, mark state complete
			self.state_set[self.dialogue_state][0] = 1
			self.dialogue_state_act = 0		
		else:
			# Otherwise, increment current utterance
			self.dialogue_state_act += 1

		# Assign current state as first zero-completion state
		for key in self.state_set:

			if (self.state_set[key][0] == 0):
				self.dialogue_state = key
				self.dialogue_state_utterance = random.choice(range(0, len(self.state_set[self.dialogue_state][1][self.dialogue_state_act]['utterances'])))
				print("Current key: " + str(self.dialogue_state) + "\tCurrent utterance index: " + str(self.dialogue_state_utterance) + "\n")
				return

		# If all states complete, default to closing
		self.dialogue_state = 'closing'

	## Automatic Speech Recognition (ASR) Methods

	# Processes text into dialogue manager
	def process_speech(self, input):
		
		# Check state iteration
		if self.proceed == True:
			print("RUNNING: Check State")
			self.check_state()

		# Do something with input
		self.current_user_utterance = input.lower()

		# Catch quit instance
		if self.current_user_utterance == 'quit':
			self.dialogue_state = 'closing'
			return

		# Prevent death spirals
		if self.cycle_timeout >= 2:
			self.dialogue_phrase = 'utterances'
			self.cycle_timeout = 0
			self.proceed = True
			return

		# # Open the pod bay doors
		# if self.current_user_utterance == 'open the pod bay doors'
		# 	# Design easter egg here
		# 	return

		print("Received input: " + self.current_user_utterance )
		print("Dialogue Phrase: " + str(self.dialogue_phrase))
		print("Dialogue State: " + str(self.dialogue_state) + "\n")

		# Only run processing on select states
		if self.dialogue_state in ('resume', 'job', 'eligibility'): # ('resume', 'job', 'eligibility')

			# Check if user input makes sense
			if self.dialogue_phrase == 'utterances' and self.validation == True:

				# Prepare to not check standard input
				self.validation = False

				# Check for matching patterns
				for key in self.state_set[self.dialogue_state][1][self.dialogue_state_act]['patterns']:
					print("Key: " + str(key) + "\n")

					# Compile regex pattern and check for match
					pattern = self.state_set[self.dialogue_state][1][self.dialogue_state_act]['patterns'][key]
					if re.search(pattern, self.current_user_utterance):
						print("Key Matched: " + str(key))

						self.user_response = key
						# Get matching value
						match = pattern.findall(self.current_user_utterance)
						self.user_response_value = str(match[0][0])
						
						#self.bad_entry = False

						self.dialogue_phrase ='grounding'
						self.proceed = False

						# End process
						return


				self.dialogue_phrase = 'bad_entry'
				self.proceed = False
				# End process
				return

			elif self.dialogue_phrase == 'utterances':
				# Prepare to check input next round
				self.validation = True
				self.proceed = False

				# Return now
				return

			# Otherwise reconcile grounding or bad state
			elif self.dialogue_phrase == 'grounding':
				
				# Check for affirmative string
				pattern = affirmative_patterns
				if re.search(pattern, self.current_user_utterance):
					match = pattern.findall(self.current_user_utterance)
					self.user_response_value = str(match[0][0])

					# Iterate dialogue state
					self.proceed = True
					self.cycle_timeout = 0
					self.utterances = True

					# End process
					return

				self.dialogue_phrase = 'utterances'
				self.cycle_timeout += 1
				self.proceed = False

				# End process
				return
			
			elif self.dialogue_phrase == 'bad_entry':

				# Set back to utterances, don't iterate, and retry
				self.dialogue_phrase == 'utterances'
				self.cycle_timeout += 1
				self.proceed = False

				# End process
				return

		# Iterate dialogue state
		self.proceed = True
		self.dialogue_phrase = 'utterances'
		self.cycle_timeout = 0

		# End process
		return

	## Speech Synthesis Methods
	
	# Selects utterance to use
	def speak(self):

		# Check timeout
		#self.__check_timeout()

		print("System: dialogue_state=" + str(self.dialogue_state))
		print("System: dialogue_state_act=" + str(self.dialogue_state_act))
		print("System: dialogue_phrase=" + str(self.dialogue_phrase))

		# Update dialogue acts
		#self.__update_dialogue_acts()

		# Update current system utterance
		self.current_system_utterance = random.choice(self.state_set[self.dialogue_state][1][self.dialogue_state_act][self.dialogue_phrase]) # [self.dialogue_state_utterance]

		if self.dialogue_phrase == 'grounding':
			self.current_system_utterance = self.current_system_utterance + str(self.user_response_value) + "?"

		# Log system utterance
		print("System: " + str(self.current_system_utterance))

		# Return system utterance to front-end
		return(self.current_system_utterance)
	