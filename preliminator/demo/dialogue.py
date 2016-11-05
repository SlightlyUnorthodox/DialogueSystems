import nltk
import datetime
import threading, time 

from .models import Candidate, Interview, User, Recruiter, PreSurvey, PostSurvey, Transcript, Feedback

# Reflections were pulled from the NLTK source code for the chat package
#http://www.nltk.org/_modules/nltk/chat/util.html#Chat

# Reflections take in user utterances and chooses what
# words to swap out during the answer
# i.e. If te candidate says "I am a junior in high school"
# then the system would swap out "i am" for "you are" in the
# response so the resonse would be something like
# "you are a junior in high school, thank you for your response"
# obviously we would like the convo to sound as natural as possible

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

# Define dialogue pairs for each state

# Greeting state pairs
greeting_pairs =  (
	
)

# Resume-driven pairs
resume_pairs = (

)

# Job-driven pairs
job_pairs = (

)

# Eligibility pairs
eligibility_pairs = (

)

# Closing state pairs
closing_pairs = (

)
class DialogueManager:
	def __init__(self, candidate_id = 1, interview_id = 1):
		# Dialogue time variables
		self.time_format = '%Y-%m-%d %H:%M:%S'
		self.start_time = datetime.datetime.now()
		self.start_time_formatted = time.mktime(datetime.datetime.strptime(self.start_time, self.time_format).timetuple())
		self.current_time = datetime.datetime.now()
		self.max_time = 3 # Max 3 minutes
		
		# Dialogue information fields
		self.candidate_id = candidate_id
		self.candidate = Candidate.objects.get(candidate_id = int(candidate_id))
		self.interview_id = interview_id
		self.interview = Interview.objects.get(interview_id = int(interview_id))

		# Dialogue state information
		self.system_state = 'Speaking'
		self.current_state = 'Greeting'
		self.end_state = 'Closing'
		self.initiative = 'System'
		self.current_speaker = 'System'

	def check_timeout(self):
		# If difference in start and current time is greater than max
		#	send signal to cancel process.

		# Renew current time
		self.current_time = datetime.datetime.now()
		current_time_formatted = time.mktime(datetime.datetime.strptime(self.current_time, self.time_format).timetuple())

		# Check dif
		if((int(current_time_formatted - self.start_time_formatted) / 60) > self.max_time) {
			# System has surpassed max time
			return(1)
		}
		
		# System still has time
		return(0)

	def generate_speech(utterance):
		# Call to speech synthesis api

	def process_speech():
		# Receive call from ASR api

	def speak(self, utterance):

		# Print to console
		print("System:" + utterance)

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

	def listen(self):



	def run(self):

		# Log demo run text
		print("Preliminator\n------------")
		print("Carry out pre-screening interview by typing or speaking in plain English.\n")
		print("When done, type or say, 'quit'.")

		# Print/Speak opening line
		self.speak(str("Hello " + self.candidate_id.first_name + ". My name is Preliminator. I will be conducting a brief screening interview today."))

		while 1:

			# If system state is 'Speaking', use system initiative
			if(self.system_state == 'Speaking')

				# If state is 'closing' run final line, else continue interview
				if (self.current_state == 'Closing'):
					self.speak()
				else:
					self.speak()

			# If system state is 'Listening', use user initiative
			else:
				input_utterance = self.listen()
				
				# If 'quit' entered, exit dialogue
				if(input_utterance.lower() == "quit"):
					return(0)

			# Check for end conditions

			# Timeout
			if(self.check_timeout() == 1) {
				break
			}

			# State based (needs refinement)
			# if(self.current_state == "Closing") {
			# 	break
			# }

