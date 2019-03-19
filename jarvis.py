# NOTE: this example requires PyAudio because it uses the Microphone class
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition as sr
from gtts import gTTS
import os
from time import localtime

# Create a new chat bot named 'INSERT NAME'
chatbot = ChatBot('INSERT NAME')
chatbot.storage.drop()

trainer = ListTrainer(chatbot)
trainer.train(open("jarvisScript.txt", "r").readlines())

#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train('chatterbot.corpus.english')


#define some key words
tools = ["saw", "screwdriver", "bolt", "screw", "hammer", "knife", "nail"]
bringWords = ["bring", "get", "fetch", "grab", "have", "give", "hand", "pass"]
returnWords = ["return", "put away", "back", "put back", "put", "away"]
abusiveWords = ['dumb','suck','idiot'] #Make this list as colorful as you'd like
noResponseWords = ['okay', 'good', 'yes', 'wonderful', 'great', 'terrific', 'nice']

# obtain audio from the microphone
r = sr.Recognizer()

#main loop
done = False
while done == False:
	#Tracks whether a "bring" or "return" keyword was used, and whether a tool was mentioned
	_bring = False
	_return = False
	_tool = ""
	#Tracks whether abusive words were mentioned, or a command was given that does not warrant a response
	_abusive = False
	_noResponse = False
	#Tracks whether there was any conflict 
	conflict = False
	#Stores the voice command
	command = ""
	
	
	with sr.Microphone() as source:
		print("\n\n\nSay something!")
		audio = r.listen(source)
	
	# recognize speech using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use 'r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")'
		# instead of 'r.recognize_google(audio)'
		command = r.recognize_google(audio)
		print(command)
	except sr.UnknownValueError:
		print("Speech Recognition could not understand audio")
		continue
	except sr.RequestError as e:
		print("Could not request results from Speech Recognition service; {0}".format(e))
		continue
	


	#command = input("\nsay something! \n")
	
	#Checks for abusive language
	for word in abusiveWords:
		if word in command.lower():
			_abusive = True
			
	#Checks for a command that does not warrant a response
	for word in noResponseWords:
		if command.lower() == word:
			_noResponse = True
	
	#Checks for a tool word
	for tool in tools:
		if tool in command.lower():
			if _tool == "":
				_tool = tool
			else:
				#Checks if one of the words is a subset of the other, and goes with the larger one
				if tool in _tool:
					_tool = _tool
				elif _tool in tool:
					_tool = tool
				else:
					conflict = True
					print("Two tools where mentioned")
	
	#Checks for "bring" synonyms
	for word in bringWords:
		if word in command.lower():
			if _return == False:
				_bring = True
			else:
				conflict = True

	#Checks for "return" synonyms
	for word in returnWords:
		if word in command.lower():
			if _bring == False:
				_return = True
			else:
				conflict = True
				
	#print(_bring, _return, _tool)
	
	#Makes sure a tool was mentioned, and that there is a "bring" or "return" word
	if (_tool == "" or (_bring == False and _return == False)):
		conflict = True
	
	#Print response
	if "shut down" in command.lower():
		response = "Shutting down"
		done = True
	elif _noResponse == True:
		response = ""
	elif "thank" in command.lower():
		response = "you're welcome!"
	elif "what time is it" in command.lower():
		hr = localtime()[3]
		min = localtime()[4]
		if hr > 12:
			hr = hr - 12
			ampm = "PM"
		else:
			ampm = "AM"
		response = "It's " + str(hr) + " " + str(min) + " " + ampm
	#Does conversions
	elif command.lower().split(" ")[0] == "convert": #convert 10 inches to meters
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
		try:
			val = float(command.lower().split(" ")[1])
			unit1 = brevDict[command.lower().split(" ")[2]]
			unit2 = command.lower().split(" ")[4]
						
			conversion = float(conversionDict[unit2]) / float(conversionDict[unit1])
			response = str(val) + " " + unit1 + " equals " + str(round(val*conversion,3)) + "  " + unit2
		except:
			response = "Sorry, I didn't understand that."
	elif _abusive == True:
		response = "Don't speak to me like that"
	elif conflict == False:
		if _bring == True:
			response = "Okay, I'll bring you the " + _tool
		elif _return == True:
			response = "Okay, I'll put the " + _tool + " away"
		else:
			response = "Error in the code, this should never happen"
	else:
		response = str(chatbot.get_response(command))
		#response = "Sorry, I didn't understand that."
	
	
	#Print and say the response
	print("response: " + response)
	
	if response != "":
		tts = gTTS(text=response, lang='en')
		tts.save("good.mp3")
		os.system("afplay good.mp3")
	


