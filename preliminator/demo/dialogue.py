import nltk
import datetime
import threading

#from .models import Candidate, Interview, User, Recruiter, PreSurvey, PostSurvey, Transcript, Feedback

# Reflections were pulled from the NLTK source code for the chat package
#http://www.nltk.org/_modules/nltk/chat/util.html#Chat

# Reflections take in user utterances and chooses what
# words to swap out during the answer
# i.e. If te candidate says "I am a junior in high school"
# then the system would swap out "i am" for "you are" in the
# response so the resonse would be something like
# "you are a junior in high school, thank you for your response"
# obviously we would like the convo to sound as natural as possible

# TODO: Expand as more patterns are identified
affirmative_patterns = "(?:[\s]|^)(yes|mhm|uhuh)(?=[\s]|$)"
negative_patterns = "(?:[\s]|^)(no)(?=[\s]|$)"

# From NLTK chatbot
reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"

}

# Define dialogue pairs (prompt-response) for each state

# Greeting state pairs
greeting_pairs =  (
	''	
)

# Resume-driven pairs
resume_pairs = (

)

# Job-driven pairs
job_pairs = (

)

# Eligibility pairs
eligibility_pairs = (
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
closing_pairs = (
	
)

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
		#self.candidate = Candidate.objects.get(candidate_id = int(candidate_id))
		self.interview_id = interview_id
		#self.interview = Interview.objects.get(interview_id = int(interview_id))

		# Dialogue interface
		self.spoken = False

		# Dialogue state information
		self.system_state = 'Speaking'
		self.current_state = 'Greeting'
		self.end_state = 'Closing'
		self.initiative = 'System'
		self.current_speaker = 'System'

		# Dialogue component space information
		self.state_set = {
			0: ['greeeting', 0], # 0 - incomplete, 1 - complete
			1: ['resume', 0],
			2: ['job', 0],
			3: ['eligibility', 0],
			4: ['conclusion', 0]
		}

		# Dialogue feature sets
		self.resume_set = {
			0: ['First Name', 0], # 0 - incomplete, 1 - complete
			1: ['Last Name', 0],
			2: ['Highest Education', 0],
			3: ['Education Status', 0],
			4: ['Major/Field', 0],
			5: ['Years Experience', 0],
			6: ['Relevant Employer', 0],
			7: ['Relevant Job Title', 0]
		}

		self.skills_set = {
			0: ["Java", 0], # 0 - na, 1-5 (strongly disagree to strongly agree)
			1: ["C++", 0],
			2: ["Databases", 0],
			3: ["Git", 0],
			4: ["", 0]
		}

		self.eligibility_set = {
			0: ["citizen", 0], # 0 - na, 1 - no, 2 - yes
			1: ["visa", 0], # 0 - na, 1 - not needed, 2 - needed
			2: ["disability", 0], # 0 - na, 1 - no, 2 - yes
			3: ["veteran", 0], # 0 - na, 1 - no, 2 - yes
		}

	def check_timeout(self):
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

	def generate_speech(self, utterance):
		# Call to speech synthesis api

		return(0)

	def process_speech(self):
		# Receive call from ASR api

		return(0)

	def speak(self):

		# Check system state

		try:
			# Start to generate speech for utterance
			thread.start_new_thread()

			# Keep thread open for interruption or timeout
			thread.start_new_thread()
		except:
			# Generate speech set for interruption
			generate_speech(state = "Interrupted")
		while 1:
			pass


		# Change system state
		self.system_state = 'Listening'

		return(0)

	def listen(self):

		return(0)

	def run(self):

		# Log demo run text
		print("Preliminator\n------------")
		print("Carry out pre-screening interview by typing or speaking in plain English.\n")
		print("When done, type or say, 'quit'.")

		# Print/Speak opening line
		# TODO: Uncommend
		#self.generate_speech(str("Hello " + self.candidate_id.first_name + ". My name is Preliminator. I will be conducting a brief screening interview today."))
		self.generate_speech(str("Hello Candidate. My name is Preliminator. I will be conducting a brief screening interview today."))
		
		# Start dialogue
		while 1:

			# If system state is 'Speaking', use system initiative
			if(self.system_state == 'Speaking'):

				self.speak()

			# If system state is 'Interrupted', use user initiative
			elif (self.system_state == 'Interrupted'):
				
				# Response to interrupted with query
				self.generate_speech("Yes?")

				# Set state to 'Listenening'
				self.system_state = 'Listening'

			# If system state is 'Listening', use user initiative
			else:

				input_utterance = self.listen()
				
				# If 'quit' entered, exit dialogue
				if(input_utterance.lower() == "quit"):
					return(0)

			# Check for end conditions

			# Timeout
			if(self.check_timeout() == 1):
				self.system_state = 'Conclusion'
			

			# State based (needs refinement)
			# if(self.current_state == "Closing"):
			# 	break
			# 


dlg = DialogueManager()
dlg.run()