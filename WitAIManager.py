from wit import Wit
import calendar
import datetime
import manager
import sys
import cStringIO
import logging
import os

access_token = os.environ.get('wit_token',open("wit_token.txt").read().strip())


def send(request, response):
    print(response['text'])

def merge(request): #meant to keep conversational context within wit.ai
	log("merge: " + str(request))

	context = request['context'] #retrieve previously stored information
	entities = request['entities'] #retrieve new information
	for key in entities.keys():
		# key = entities.keys()[0] #get the list of all the keys stored in the first index of the dictionary
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
	This definition is meant to combine all the information collected from the user. 
	This informtion is stored in 'context' and includes the class name of the assignment, the assignment name, and the day it is due.
	This is printed to the screen
	'''
	log("adding a class: " + str(request))
	context = request['context']
	course = context['class']
	name =  context['assignment_name']
	date = context['datetime']
	phone_number = context['user']

	added_assignment = manager.add_assignment(phone_number, name, date, course)

	context['datetime'] = added_assignment.get_pretty_date()
	# context['datetime'] = beautiful_date(date)
	return context

def twilio_input(context, message):
	phone_number = context['user']
	current_user = manager.get_user(phone_number)
	session_id = current_user.get_session_id()
	
	stdout_ = sys.stdout #Keep track of the previous value.
	stream = cStringIO.StringIO()
	sys.stdout = stream
	new_context = client.run_actions(session_id, message, context, max_steps=10)
	sys.stdout = stdout_ # restore the previous stdout.
	print 'new context =' + str(new_context)
	return {'resp':stream.getvalue(), 'context': new_context} # This will get the string inside the variable


def display_all_assignments(request):
	context = request['context']
	assignments = manager.get_all_assignments(request)
	pretty_response = ''
	if len(assignments) > 0:
		for i in assignments:
			pretty_response += i.to_string() + "\n"
		context['pretty_response'] = pretty_response
	elif context.has_key('inspirational_quote'):
		context
	else:
		context['empty'] = True
	log("display all: " + str(request))
	return context


def display_assignments_by_class(request):
	log("display assignment by class: " + str(request))
	context = request['context']
	assignments = manager.get_assignments_of_course(request)
	pretty_response = ''
	if(len(assignments) > 0):
		for i in assignments:
			pretty_response += i.to_string() + "\n"
		context['pretty_response'] = pretty_response
	else:
		context['empty'] = True
	return context


def display_assignments_by_type(request):
	log("display assignment by type: " + str(request))
	context = request['context']
	assignments = manager.get_assignments_of_type(request)
	pretty_response = ''
	if(len(assignments) > 0):
		for i in assignments:
			pretty_response += i.to_string() + "\n"
		context['pretty_response'] = pretty_response
	else:
		context['empty'] = True
	return context

def display_assignments_by_date(request):
	log("display assignment by date: " + str(request))
	context = request['context']
	assignments = manager.get_assignments_up_to_date(request)
	pretty_response = ''
	if(len(assignments) > 0):
		for i in assignments:
			pretty_response += i.to_string() + "\n"
		context['pretty_response'] = pretty_response
	else:
		context['empty'] = True
	return context

def delete_assignment(request):
	log("delete assignment: " + str(request))
	context = request['context']
	if(manager.delete_assignment(request)):
		context = display_all_assignments(request)
	else:
		context['did_not_delete'] = True
	return context

#clear context, only leaving user phone #
#also will increment user session counter
def clear_context(request):
	log("cleared context: " + str(request))

	context = request['context']

	phone_number = context['user']
	current_user = manager.get_user(phone_number)
	current_user.increment_session()

	context = {"user":context["user"]}
	return context

def generate_sentences(request):
	log("motivational sentence: " + str(request))
	phone_number = request['context']['user']
	context = {'user':phone_number}
	context['inspirational_quote'] = mcc.get_sentence()
	return context

def log(message):
	logfile = open('log.txt').read() + "\n"
	current_time = datetime.datetime.now().time()
	logfile += (str(current_time) + " : " + message + "\n")
	log_to_write = open('log.txt', 'w')
	log_to_write.write(logfile)
	log_to_write.close()
	
def save_to_s3():
	manager.backup()

def load_from_s3():
	manager.load()
		
actions = {
    'send': send,
    'merge': merge,
    'add_class': add_class,
    'display_all_assignments':display_all_assignments,
    'display_assignments_by_class': display_assignments_by_class,
    'display_assignments_by_type':display_assignments_by_type,
    'display_assignments_by_date':display_assignments_by_date,
    'clear_context':clear_context,
    'delete_assignment':delete_assignment,
}

client = Wit(access_token=access_token, actions=actions)
client.logger.setLevel(logging.WARNING)
