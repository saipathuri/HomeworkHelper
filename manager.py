import user
from passlib.hash import pbkdf2_sha256

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
		return users['phone_number']
	except KeyError:
		raise Exception("User doesnt exist")

"""
create usere with the given phone number and password
"""
def add_user(phone_number, password):
	users[phone_number] = user.create_user(phone_number, _hash(password))


"""
adds assignment to user with the given phone number
assignment must be of type assignment
"""
def add_assignment(phone_number, assignment):
	user = get_user(phone_number)
	user.add_assignment(assignment)

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