import nltk
import datetime
import threading
#import views
import collections

from .models import Candidate, Interview, User, Recruiter, PreSurvey, PostSurvey, Transcript, Feedback

# TODO: Expand as more patterns are identified
affirmative_patterns = "(?:[\s]|^)(yes|mhm|uhuh)(?=[\s]|$)"
negative_patterns = "(?:[\s]|^)(no)(?=[\s]|$)"
likert_patterns_one =  "(?:[\s]|^)(one)(?=[\s]|$)"
likert_patterns_two =  "(?:[\s]|^)(two)(?=[\s]|$)"
likert_patterns_three =  "(?:[\s]|^)(three)(?=[\s]|$)"
likert_patterns_four =  "(?:[\s]|^)(four)(?=[\s]|$)"
likert_patterns_five =  "(?:[\s]|^)(five)(?=[\s]|$)"
gpa_patterns = "(?:[\s]|^)(point)(?=[\s]|$)"

class DialogueManager:
	def __init__(self, candidate_id = 1, interview_id = 1):

		# Dialogue time variables
		self.start_time = datetime.datetime.now()
		self.current_time = datetime.datetime.now()
		self.run_time = 0
		self.max_time = 3 # Max 3 minutes

		# Dialogue information fields
		# NOTE: using try/catch to handle testing outside of Django instance
		self.candidate_id = candidate_id
		self.interview_id = interview_id
		self.candidate = Candidate.objects.get(candidate_id = int(candidate_id))
		self.interview = Interview.objects.get(interview_id = int(interview_id))

		# Dialogue interface
		self.spoken = False

		# Dialogue state information
		self.system_state = 'speaking'
		self.current_state = 'greeting'
		self.current_state_utterance = 0
		self.end_state = 'closing'
		self.initiative = 'system'
		self.current_speaker = 'system'

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
		self.greeting_pairs =  (
			( "Hello " + str(self.resume_set['first_name'][1]) + ", my name is Preliminator. We'll be conducting a brief interview today. Ready to begin?",
			{
				"name": "any input",
			}),
		)

		# Resume-driven pairs
		self.resume_pairs = (
			( "I didn't see you enter your GPA, to the best of your knowledge, what is your current GPA?",
				{
					"gpa": gpa_patterns,
				}),
		)

		# Job-driven pairs
		self.job_pairs = (
			( "On a scale of 1 to 5, 'one' being no experience and five 'expert', what level of experience would you say you have with Git?",
				{
				 1: likert_patterns_one,
				 2: likert_patterns_two,
				 3: likert_patterns_three,
				 4: likert_patterns_four,
				 5: likert_patterns_five,
				}),
		)

		# Eligibility pairs
		self.eligibility_pairs = (
			( "Are you a United States citizen?",
				{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				}),
			( "Will you at any time require visa-sponsorship to continue working?",
				{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				}),
			( "Are you a protected veteran?",
				{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				}),
			( "Have you ever been convicted of a felony?",
				{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				}),
			( "Do you require any disability-related accomodations?",
				{
				 "yes": affirmative_patterns,
				 "no": negative_patterns,
				}),
		)

		# Closing state pairs
		self.closing_pairs = (
			( "Well I believe we are out of time. Thank you for taking the time to try the Preliminator demo and have a good day.",
				{
				"any":"any pattern",
				}),

		)

		# Dialogue component space information
		self.state_set = collections.OrderedDict([
			('greeting', [0, self.greeting_pairs]), # 0 - incomplete, 1 - complete
			('resume', [0, self.resume_pairs]),
			('job', [0, self.job_pairs]),
			('eligibility', [0, self.eligibility_pairs]),
			('closing', [0, self.closing_pairs]),
		])

		# Store recent utterances
		self.current_system_utterance = ""
		self.current_user_utterance = ""

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

	def check_state(self):

		# Check to see if current state has remaining utterances ## TODO: make more sophisticated
		if ((self.current_state_utterance + 1) >= len(self.state_set[self.current_state][1])):
			# If no more utterances, mark state complete
			self.state_set[self.current_state][0] = 1
			self.current_state_utterance = 0		
		else:
			# Otherwise, increment current utterance
			self.current_state_utterance += 1

		# Assign current state as first zero-completion state
		for key in self.state_set:
			#print("Key: " + key)
			#print(self.state_set[key][0])

			if (self.state_set[key][0] == 0):
				self.current_state = key
				print("Current key: " + str(self.current_state) + "\tCurrent utterance index: " + str(self.current_state_utterance) + "\n")
				return

		# If all states complete, default to closing
		self.current_state = 'closing'

		print("Current key: " + str(self.current_state) + "\tCurrent utterance index: " + str(self.current_state_utterance) + "\n")
		return

	## Automatic Speech Recognition (ASR) Methods
	
	# Recieves text from API
	def listen(self):
		
		# TODO: Implement back into views
		#current_user_utterance = views.receive_chat_text

		# Use text listener for now
		user_input = raw_input()

		# Pass input to dialogue manager for parsing
		self.process_speech(user_input)

	# Processes text into dialogue manager
	def process_speech(self, input):
		
		# Do something with input

		# Change system state
		self.system_state = 'speaking'

		return(0)

	## Speech Synthesis Methods
	
	# Sends selected text to speech synthesis API
	def generate_speech(self, utterance):
		# Call to speech synthesis api
		# we don't want to make the http rsponse live here though
		print("System: " + str(utterance) + "\n")

		return(utterance)

	# Selects utterance to use
	def speak(self):

		# Check system state

		# TODO: Implement multi-threading for interruption listener
		# try:
		# 	# # Start to generate speech for utterance
		# 	# thread.start_new_thread()

		# 	# # Keep thread open for interruption or timeout
		# 	# thread.start_new_thread()
		# except:
		# 	# Generate speech set for interruption
		# 	self.generate_speech(utterance = "Yes?")

		# while 1:
		# 	pass

		self.current_system_utterance = self.state_set[self.current_state][1][self.current_state_utterance][0]

		system_utterance = self.generate_speech(utterance = self.current_system_utterance)
		
		# Change system state
		self.system_state = 'listening'

		return(system_utterance)
	
	## Run Dialogue Manager

	def run(self):

		# Log demo run text
		print("Preliminator\n------------")
		print("Carry out pre-screening interview by typing or speaking in plain English.\n")
		print("When done, type or say, 'quit'.\n\n")

		# Print/Speak opening line
		# TODO: Uncommend
		#self.generate_speech(str("Hello " + self.candidate_id.first_name + ". My name is Preliminator. I will be conducting a brief screening interview today."))
		#self.generate_speech(str("Hello Candidate. My name is Preliminator. I will be conducting a brief screening interview today."))
		#self.state_set['greeting'][0] = 1

		# Start dialogue
		while 1:

			print("System state = " + self.system_state)
			print("Current state = " + self.current_state + "\n")

			# If system state is 'Speaking', use system initiative
			if(self.system_state == 'speaking'):
				
				self.speak()

			# If system state is 'Interrupted', use user initiative
			elif (self.system_state == 'interrupted'):
				
				# Response to interrupted with query
				self.generate_speech("Yes?")

				# Set state to 'Listenening'
				self.system_state = 'listening'

			# If system state is 'Listening', use user initiative
			else:
			
				self.listen()

				# If 'quit' entered, exit dialogue
				if(self.current_user_utterance == "quit"):
					return(0)

			# Check for end conditions

			# Timeout
			if(self.__check_timeout() == 1):
				print("System Concluding\n")
				self.system_state = 'closing'


			# State based (needs refinement)
			if(self.current_state == 'closing'):
			 	return(0)
			


			self.__check_state()


# dlg = DialogueManager()
# dlg.run()
