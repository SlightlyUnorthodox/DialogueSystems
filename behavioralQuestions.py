# so i am aware this file has no structure or anything
# this eventually could be the file where we link 
# the responses and questions to the rest of the code
# for now i felt like it be helpful just to have some questions
# since we will need them eventually
# typing them all out will be time consuming, so why not start now


# set up like that chatbot code Dax showed me from eliza system
# categories are teamwork, Client-Facing Skills, Adapting,
# Time management, and Communication

#TODO finish filling in the q's

responses = (
	(r'Teamwork (.*)',
	  ("Talk about a time when you had to work closely with someone whose personality was very different from yours. How did you handle it %1?",
	   "Give me an example of a time you faced a conflict while working on a team. How did you handle that %1?",
	   "Describe a time when you struggled to build a relationship with someone important. How did you eventually overcome that %1?",
	   "We all make mistakes we wish we could take back. Tell me about a time you wish you’d handled a situation differently with a colleague and how you handled it %1?",
	   "Tell me about a time you needed to get information from someone who wasn’t very responsive. What did you do %1?")),

	(r'Client-Facing Skills (.*)',
		("Describe a time when it was especially important to make a good impression on a client. How did you go about doing so %1?",
		 "Give me an example of a time when you did not meet a client’s expectation. What happened, and how did you attempt to rectify the situation %1?",
		 "Tell me about a time when you made sure a customer was pleased with your service. How did you do that %1?",
		 "Describe a time when you had to interact with a difficult client. What was the situation, and how did you handle it %1?")),

	(r'Adapting (.*)',
		
	))
)