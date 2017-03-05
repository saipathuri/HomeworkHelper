from wit import Wit
import calendar
import datetime

access_token = open("wit_token.txt").read()

def send(request, response):
    print(response['text'])

def merge(request): #meant to keep conversational context within wit.ai
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

def add_class(request): 
	'''
	This definition ieant to combine all the information collected from the user. 
	This informtion is stored in 'context' and includes the class name of the assignment, the assignment name, and the day it is due.
	This is printed to the screen
	'''
	context = request['context']
	print context['class']
	print context['assignment_name']
	context['datetime'] = beautiful_date(context['datetime'])
	print context['datetime']
	return context

def beautiful_date(date_str):
	date = datetime.datetime.strptime(date_str.split("T")[0], "%Y-%m-%d").date()
	date_str = str(calendar.month_name[date.month])
	date_str += " " + str(date.day) + ", " + str(date.year)
	return date_str

actions = {
    'send': send,
    'merge': merge,
    'add_class': add_class,
}

access_token = "ABPNWDEXGLNGHP6J7VKEZKBZMFHXNJG4";
client = Wit(access_token=access_token, actions=actions)
client.interactive()