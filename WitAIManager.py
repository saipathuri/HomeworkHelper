from wit import Wit
import calendar
import datetime
import manager
import sys
import cStringIO

access_token = open("wit_token.txt").read().strip()
# test_number = open("test_number.txt").read().strip()


def send(request, response):
    print(response['text'])

def merge(request): #meant to keep conversational context within wit.ai
	try:
		context = request['context'] #retrieve previously stored information
		entities = request['entities'] #retrieve new information
		key = entities.keys()[0] #get the list of all the keys stored in the first index of the dictionary
		list_type_to_merge = entities[key] #get the list of all the items stored in the specified key
		entity_name = "" #lmao wtf
		for i in range(0,len(list_type_to_merge)): #go from 0 to the number of items stored in the specified key
			type_to_merge = list_type_to_merge[i] #save a specific section of the list to a single variable
			if i < len(list_type_to_merge)-1: #if the list_type_to_merge isn't being read at the last variable, add a space to the end of the word
				entity_name += type_to_merge['value'] + " "
			else:
				entity_name += type_to_merge['value'] #if it is being read at the end of the last variable, don't add a space
		context[key] = entity_name
		return context #return all the gucci INFO
	except IndexError:
		print "Sorry, we didn't catch that. Can you try again?"

def add_class(request): 
	'''
	This definition is meant to combine all the information collected from the user. 
	This informtion is stored in 'context' and includes the class name of the assignment, the assignment name, and the day it is due.
	This is printed to the screen
	'''
	context = request['context']
	course = context['class']
	name =  context['assignment_name']
	date = context['datetime']
	phone_number = context['user']

	manager.add_user(phone_number, "test_password")
	manager.add_assignment(phone_number, name, date, course)

	context['datetime'] = beautiful_date(date)
	return context

def beautiful_date(date_str):
	date = datetime.datetime.strptime(date_str.split("T")[0], "%Y-%m-%d").date()
	date_str = str(calendar.month_name[date.month])
	date_str += " " + str(date.day) + ", " + str(date.year)
	return date_str

def twilio_input(context, message):
	session_id = context['user']
	
	stdout_ = sys.stdout #Keep track of the previous value.
	stream = cStringIO.StringIO()
	sys.stdout = stream
	new_context = client.run_actions(session_id, message, context, max_steps=10)
	sys.stdout = stdout_ # restore the previous stdout.
	return {'resp':stream.getvalue(), 'context': new_context} # This will get the string inside the variable



actions = {
    'send': send,
    'merge': merge,
    'add_class': add_class,
}

client = Wit(access_token=access_token, actions=actions)