# brings the pieces together
import chatUtil as util 

# creates the conversation class that will pass along the information we need



class Conversation(object):
    generatedString = "";

	def __init__(self, responses, reflections={}):
        
        # below is pulled from the nltk documentation website
        # pairs is a list of patterns and its responses
        # each pattern is a regex that matches user statement or q
        # ex: r'I want (.*)' then a list of answers is then given like
        # "why do you want %1"
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self.responses = [(re.compile(x, re.IGNORECASE),y) for (x,y) in responses]
        self.reflections = reflections
        self.regex = self.compileReflections()

    def replace(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self.regex.sub(lambda mo:
                self.reflections[mo.string[mo.start():mo.end()]],
                    str.lower())


    # finds the % in the responses to insert the new response
    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self.replace(match.group(num)) + \
                response[pos+2:]
            pos = response.find('%')
        return response


    # generates our string response
    def respond(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        # check each pattern
        for (pattern, response) in self.responses:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp


    # Hold a conversation with a chatbot

    def converse(self, quit="quit"):
        input = ""
        while input != quit:
            input = quit
            try: input = compat.raw_input(">")
            except EOFError:
                print(input)
            if input:
                while input[-1] in "!.": input = input[:-1]
                print(self.respond(input))


    # create string that needs to be passed to the chat bot via a .js file
    # standy for bugs
    def createJS():
        return generatedString;
    # Hold a conversation with a chatbot



eliza_chatbot = Conversation(responses, reflections)

def eliza_chat():
    print("Therapist\n---------")
    print("Talk to the program by typing in plain English, using normal upper-")
    print('and lower-case letters and punctuation.  Enter "quit" when done.')
    print('='*72)
    print("Hello.  How are you feeling today?")

    eliza_chatbot.converse()

def demo():
    eliza_chat()

if __name__ == "__main__":
    demo()
