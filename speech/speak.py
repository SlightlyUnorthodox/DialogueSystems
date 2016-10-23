# module to handle all the verbal output by the system
import pyttsx

# forgot where to put this where it would be helpful
engine = pyttsx.init()

#def setup():

def talk(string):
	engine.say(string)
	engine.runAndWait()


