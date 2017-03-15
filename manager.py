from user import user
from assignment import assignment
from passlib.hash import pbkdf2_sha256
import datetime
import s3_manager

"""
users holds all users in the system
type: dictionary
key:phone number
value: user object
"""
users = {}

"""
returns user with the given number
"""
def get_user(phone_number):
	try:
		return users[phone_number]
	except:
		add_user(phone_number, "temp_pass")
		return users[phone_number]

def get_assignments_for_user(user):
	return user.get_assignments()


"""
create usere with the given phone number and password
"""
def add_user(phone_number, password):
	hashed_password = _hash(password)
	users[phone_number] = user().initialize_user(phone_number, hashed_password)


"""
adds assignment to user with the given phone number
assignment must be of type assignment
"""
def add_assignment(phone_number, name, date, course):
	ass_to_add = assignment()
	ass_to_add.create_assignment(name, date, course)
	user_to_modify = get_user(phone_number)
	user_to_modify.add_assignment(ass_to_add)

	#THIS RETURN IS REQUIRED FOR WITAIMANAGER
	return ass_to_add

"""
returns array of assignments that are from the course specified
"""
def get_assignments_of_course(request):
	context = request['context']
	entities = request['entities']
	phone_number = context['user']

	course = context['class']

	assignments_in_course = []

	assignments = get_assignments_for_user(get_user(phone_number))

	for ass in assignments:
		if ass.get_course() == course:
			assignments_in_course.append(ass)

	return assignments_in_course

def get_assignments_of_type(request):
	context = request['context']
	entities = request['entities']
	phone_number = context['user']

	name = context['assignment_name']

	assignments_of_type = []

	assignments = get_assignments_for_user(get_user(phone_number))

	for ass in assignments:
		if ass.get_name() == name:
			assignments_of_type.append(ass)

	return assignments_of_type

def get_assignments_up_to_date(request):
	context = request['context']
	entities = request['entities']
	phone_number = context['user']

	date_str = context['datetime']
	date_obj = assignment().create_date_obj(date_str)

	assignments_on_date = []

	assignments = get_assignments_for_user(get_user(phone_number))

	for ass in assignments:
		if ass.get_date() <= date_obj:
			assignments_on_date.append(ass)

	return assignments_on_date

def get_all_assignments(request):
	context = request['context']
	entities = request['entities']
	phone_number = context['user']
	return get_assignments_for_user(get_user(phone_number))


def delete_assignment(request):
	context = request['context']
	course = context['class']
	name = context['assignment_name']
	date_str = context['datetime']
	date_obj = assignment().create_date_obj(date_str)

	phone_number = context['user']

	assignments = get_assignments_for_user(get_user(phone_number))
	for ass in assignments:
		if ass.get_course() == course:
			if ass.get_date() == date_obj:
				if ass.get_name() == name:
					assignments.remove(ass)
					return ass

def backup():
	s3_manager.save(users)

def load():
	users = s3_manager.load()
"""
hashes password with sha256 and returns it
"""
def _hash(password):
	hash = pbkdf2_sha256.hash(password, rounds=50000, salt_size=16)
	return hash

"""
compares entered password with current password
"""
def _verify(phone_number, password):
	user = get_user(phone_number)
	current_password = user.get_password()
	return pbkdf2_sha256.verify(password, current_password)
