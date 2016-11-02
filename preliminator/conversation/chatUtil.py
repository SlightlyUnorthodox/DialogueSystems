
# pulled from this url, will change later after basic model works
#http://www.nltk.org/_modules/nltk/chat/util.html#Chat


# reflections take in user utterances and chooses what
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


# so i am aware this file has no structure or anything
# this eventually could be the file where we link 
# the responses and questions to the rest of the code
# for now i felt like it be helpful just to have some questions
# since we will need them eventually
# typing them all out will be time consuming, so why not start now


# set up like that chatbot code Dax showed me from eliza system
# categories are teamwork, Client-Facing Skills, Adapting,
# Time management, and Communication

# MAIN IDEA
#A Frame is a script-like conceptual structure that describes a 
#particular type of situation, object, or event along with the participants 
#and props that are needed for that Frame. For example, the "Apply_heat" 
#frame describes a common situation involving a Cook, some Food, and a Heating_Instrument, 
#and is evoked by words such as bake, blanch, boil, broil, brown, simmer, steam, etc.

#my thought is we treat each step in the interview as a frame. 

#TODO finish filling in the q's
# tbh no clue why the %1 is there, it was there in the eliza examples

# the phrase after the letter "r" specifies what phrase we have identified that we want to respond to
responses = (
	(r'Teamwork (.*)',
	  ("Talk about a time when you had to work closely with someone whose personality was very different from yours. How did you handle it %1?",
	   "Give me an example of a time you faced a conflict while working on a team. How did you handle that %1?",
	   "Describe a time when you struggled to build a relationship with someone important. How did you eventually overcome that %1?",
	   "We all make mistakes we wish we could take back. Tell me about a time you wish you’d handled a situation differently with a colleague and how you handled it %1?",
	   "Tell me about a time you needed to get information from someone who wasn’t very responsive. What did you do %1?")
	),

	(r'Client-Facing Skills (.*)',
		("Describe a time when it was especially important to make a good impression on a client. How did you go about doing so %1?",
		 "Give me an example of a time when you did not meet a client’s expectation. What happened, and how did you attempt to rectify the situation %1?",
		 "Tell me about a time when you made sure a customer was pleased with your service. How did you do that %1?",
		 "Describe a time when you had to interact with a difficult client. What was the situation, and how did you handle it %1?")
	),

	(r'Greeting (.*)',
		("Hello! Great to see you %1.",
		 "Hi there, nice to see you again %1.",
		 "Sup Dawg %1."
		)
	),

	(r'Closing (.*)',
		("Thank you for your time, we will get back to you as soon as HR recieves your applicatoin %1.",
		 "Thank you for your interest in the company, we will be in contact soon"
		)
	),

	(r'FieldConfirmation (.*)',
		("Thank you, your answer has been noted %1.",
		 "Great, we'll write that down %1.",
		 "Ok, thank you for your response %1."
		)
	),

	(r'Location Preference (.*)',
		("Excellent, we think you will love %1.",
		 "Great, %1.",
		 "You can't go wrong living in %1."
		)
	),

	(r'I think (.*)',
        ("That's a great opinion on that matter!",
        "Glad to see your train of thought."
        )
    ),

    (r'I\'m not sure ' (.*)',
		("Don't worry about it, thanks for your honesty.",
		 "It's ok, we just want to see your past experiences."
		)
	),

	(r'how are you (.*)',
		("Great, thank you for asking"
		)
	)

)












