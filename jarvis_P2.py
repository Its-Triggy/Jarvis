from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition as sr
from gtts import gTTS
import os, re, time
from time import localtime
import wikipedia
import subprocess


def get_wiki_def(string):
	try:
		data = wikipedia.summary(string).lower()
		data = data.replace("i.e.", "i,e,").replace("e.g.", "e,g,").replace("jr.", "jr,").replace("sr.", "sr,").replace("lit.", "lit,")
		
		definition = data.split(".")[0]+"."
		definition = re.sub(r'\(.*\)', "", definition)
		
	except:
		definition = "I'm not sure what you mean. Could you be more specific?"
	return(definition)

def get_wiki_summary(string):
	try:
		data = wikipedia.summary(string).lower()
		data = data.replace("i.e.", "i,e,").replace("e.g.", "e,g,").replace("jr.", "jr,").replace("sr.", "sr,").replace("lit.", "lit,")
		
		summary = ''
		data = data.split("\n")[0]
		
		for i, sentence in enumerate(data.split(".")[1:-1]):
			if i == 0:
				sentence = re.sub(r'\(.*\)', "", sentence)
			summary += sentence + "."
		
	except:
		summary = "I'm not sure whae you mean. Could you be more specific?"
		
	return(summary)
		
def addToScript():
	linesAdded = 0
	
	exit = False
	while exit == False:
		
		if linesAdded == 0:	
			print("You want to add a line to the script?")
			speak("You want to add a line to the script?")
		
		else:	
			print("Would you like to add another line to the script?")
			speak("Would you like to add another line to the script?")
		
		answer = listenForYesNo()
				
		if answer == "no":
			speak("Okay, no new line.")
			exit = True
			
		elif answer == "yes":
			print("Give me a line to add to the script.")
			speak("Give me a line to add to the script.")
			
			newLine = listen()

			speak("I understood " + newLine + ". Is that correct? Yes or no?")	
		
			answer = listenForYesNo()
		
			if answer == "yes":	
				file = open("jarvisScript.txt", "a")
				file.write("\n" + newLine)
				file.close()
				speak("Okay, the line was added.")
				linesAdded += 1
			else:
				speak("Okay, the line was not added.")	 
		
def speak(response):
	tts = gTTS(text=response, lang='en')
	tts.save("good.mp3")
	os.system("afplay good.mp3")	

def listen():	
	understood = False
	while understood == False:
		with sr.Microphone() as source:
			audio = r.listen(source)
		try:
			reply = r.recognize_google(audio)
			print(reply)
			understood = True
		except sr.UnknownValueError:
			print("Speech Recognition could not understand audio")
			continue		
		except sr.RequestError as e:
			print("Could not request results from Speech Recognition service; {0}".format(e))
			continue
		
	return reply

def listenForYesNo():
	theUserSaidYesOrNo = False
	while theUserSaidYesOrNo == False:
		answer = listen()

		for word in ["yes", "yeah", "yep", "yup", "affirmative", "true", "correct"]:
			if word in answer.lower():
				answer = "yes"
				theUserSaidYesOrNo = True
	
		for word in ["no", "now", "nope", "negative", "false", "incorrect"]:
			if word in answer.lower():
				answer = "no"
				theUserSaidYesOrNo = True
					
		if theUserSaidYesOrNo == False:
			speak("Sorry, I didn't catch that. Yes or No?")
					
	return answer

def conversion(_command):
	_command = command.lower().split("convert")[-1]
	
	conversionDict = {"inches":39.3701, "feet":3.2808, 
						"kilometers":.001,"meters":1, 
						"decimeters":10, "centimeters":100, 
						"millimeters":1000, "yards":1.0936, "miles":0.0006213}
	
	brevDict = {"in":"inches", "inch":"inches", "inches":"inches", "ft":"feet", 
				"foot":"feet", "feet":"feet", "km":"kilometers", "kilometer":"kilometers", 
				"kilometers":"kilometers", "m":"meters", "meter":"meters",
				"meters":"meters", "dm":"decimeters", "decimeter":"decimeters",
				"decimeters":"decimeters", "cm":"centimeters", "centimeter":"centimters",
				"centimeters":"centimeters", "mm":"millimeters", "millimeter":"millimeters",
				"millimeters":"millimeters", "yd":"yards", "yard":"yards",
				 "yards":"yards", "miles":"miles", "mile":"miles"}
	try: #5 inches to meters
		val = float(_command.lower().split(" ")[1])
		unit1 = brevDict[_command.lower().split(" ")[2]]
		unit2 = _command.lower().split(" ")[4]
					
		conversion = float(conversionDict[unit2]) / float(conversionDict[unit1])
		return (str(val) + " " + unit1 + " equals " + str(round(val*conversion,3)) + "  " + unit2)
	except:
		return ("Sorry, I didn't understand that.")
		
'''
# Create a new chat bot named 'INSERT NAME'
chatbot = ChatBot('INSERT NAME')
chatbot.storage.drop()

trainer = ListTrainer(chatbot)
trainer.train(open("jarvisScript.txt", "r").readlines())

#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train('chatterbot.corpus.english')
'''

#define some key words
wordList_dict = {"shut down" : ["shut down", "shutdown", "switch off", "turn off", "go to sleep", "good night", "goodbye", "good bye"],
				"wiki def" : ["tell me about", "who is", "what is", "define", "definition of", "who are", "what are", "short explanation"],
				"wiki summary" : ["tell me more", "continue", "go on", "tell me about"],
				"tool": ["screwdriver", "hammer", "knife", "wrench", "pliers", "wire cutters"],
				"convert" : ["convert"],
				"thanks" : ["thanks", "thank you"],
				"time" : ["what time is it", "what time it is", "the time"],
				"bring" : ["bring", "get", "fetch", "grab", "have", "give", "hand", "pass", "release", "lower"],
				"return" : ["return", "put away", "back", "put back", "put", "away", "reel in", "real in", "raise"],
				"abusive" : ['dumb','suck','idiot'], #Make this list as colorful as you'd like
				"no response" : ['wow', 'whoa', 'cool', 'okay', 'good', 'yes', 'wonderful', 'great', 'terrific', 'nice', 'oh', 'awesome', 'sounds good', 'fine'],
				"how are you" : ['how are you', 'whats up', 'what\'s up', 'what is up', 'how do you feel', 'how are you feeling'],
				"hello" : ["hello", "hi", "high"],
				"are you there" : ['are you on', 'you on', 'can you hear me', 'you there', 'are you there', 'are you listening'],
				"add to script" : ['add to script']}

# obtain audio from the microphone
r = sr.Recognizer()

#Track which items are raised and which are lowered
raised_dict = {tool : True for tool in wordList_dict["tool"]}

#Stores the subject of conversation (i.e. what we are talking about)
subject = ""

#main loop
done = False
while done == False:
	
	#Stores the voice command
	command = ""
	command = listen()
	#command = input("Say something: ")
	total_words = len(command.lower().split(" "))
	
	#Keep track of which key words were mentioned
	bool_dict = {key:False for key, value in wordList_dict.items()}
	
	
	#Check for key words in the command
	for key, value in wordList_dict.items():
		for word in value:
			if word in command.lower(): bool_dict[key] = True
		
	#Shut down 
	if bool_dict["shut down"] == True:
		response = "Shutting down"
		done = True
		
		for tool, value in raised_dict.items():
			if value == False:
				subprocess.Popen("python3 jarvis_bot.py raise,"+tool, shell=True)
				raised_dict = True

	#No response is warranted
	elif bool_dict["no response"] == True and total_words<=2:
		response = "yep"
	
	#Give wiki definition
	elif bool_dict["wiki def"] == True:
		for item in wordList_dict["wiki def"]:
			if item in command.lower():
				phrase = item
		subject = command.lower().split(phrase)[-1].replace("again","")
		response = get_wiki_def(subject)
	
	#Give longer wiki definition
	elif bool_dict["wiki summary"] == True:
		if subject != "":
			response = get_wiki_summary(subject)
		else:
			response = "tell you about what?"
		
	#Add to script
	elif bool_dict["add to script"] == True:
		addToScript()
		response = ""
	
	#Gives the current time
	elif bool_dict["time"] == True:
		hr = localtime()[3]
		min = localtime()[4]
		if hr > 12:
			hr = hr - 12
			ampm = "PM"
		else:
			ampm = "AM"
		response = "It's " + str(hr) + " " + str(min) + " " + ampm
	
	#Does conversions (e.g. convert 10 inches to meters)
	elif bool_dict["convert"] == True: 
		response = conversion(command)
	
	#Says you're welcome
	elif bool_dict["thanks"] == True:
		response = "you're welcome!"
	
	#Addresses abusive language
	elif bool_dict["abusive"] == True:
		response = "Don't speak to me like that"
	
	#Answers "how are you"
	elif bool_dict["how are you"] == True:
		response = "I am doing well!"
	
	#Answers "hello"
	elif bool_dict["hello"] == True and total_words<=2:
		response = "Hi there!"
	
	#Answers "are you there" with yes
	elif bool_dict["are you there"] == True:
		response = "yes, I am listening!"
	
	#Bring whichever tools were requested		
	elif bool_dict["tool"] and bool_dict["bring"] and bool_dict["return"]==False:				
		tools = [] 	#collect tools that were mentioned
		for word in wordList_dict["tool"]:
			if word in command.lower(): tools.append(word)
		
		response = ""
		for tool in tools:
			if raised_dict[tool]==True:
				raised_dict[tool]=False
				response += "Bringing you the " + tool + ". \n"
				subprocess.Popen("python3 jarvis_bot.py lower,"+tool, shell=True)
			else:
				response += "The " + tool + " is already out. \n"

	#Return whichever tools were requested		
	elif bool_dict["tool"] and bool_dict["return"] and bool_dict["bring"]==False:				
		tools = [] 	#collect tools that were mentioned
		for word in wordList_dict["tool"]:
			if word in command.lower(): tools.append(word)
		
		response = ""
		for tool in tools:				
			if raised_dict[tool]==False:
				raised_dict[tool]=True
				response += "Putting away the " + tool + ". \n"
				subprocess.Popen("python3 jarvis_bot.py raise,"+tool, shell=True)
			else:
				response += "The " + tool + " is already put away. \n"
	
	else:
		'''response = str(chatbot.get_response(command))'''
		response = "Sorry, I didn't understand that." 
	
	#Print and say the response
	print("response: " + response)
	speak(response)
	