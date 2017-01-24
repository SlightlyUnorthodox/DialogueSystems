from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import *

from nltk.chat.util import Chat, reflections
from nltk.chat.rude import pairs

import time

test_chatbot = Chat(pairs, reflections)

def index(request):
    return HttpResponse("Hello, world. You're at the dialouge index.")

def dialogue(request):
	# Initialize dialogue manager
	
	# Hacky solution to start things
	return render(request, 'chat.html', {'interview':request.session.get('interview', None)})

@csrf_exempt
def process_ajax(request):


	# Attempt to retrive input text from interview page
	if request.method == 'POST': # and request.is_ajax():
		if 'inputText' in request.POST:
			user_utterance = request.POST['inputText']
		else:
			return HttpResponse('Missing User Input')
	else:
		return HttpResponse('Bad Request')

	# Process user utterance
	#dm.process_speech(input = user_utterance)

	# Arbitrary delay to simulate processing.
	time.sleep(0.5)


	# Render utterance to screen
	return HttpResponse(test_chatbot.respond(str(user_utterance).lower()))
