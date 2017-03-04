import assignment

class user(object):

	def __init__(self):
		self.phone_number = "+15556667777"
		self.assignments = []
		self.password = ""

	def create_user(phone_number, password):
		self.phone_number = phone_number
		self.password = password

	def add_assignment(assignment):
		if isinstance(assignment, assignment):
			self.assignments.append(assignment)
		else:
			raise TypeError("Must be of type assignment")

	def get_assignments():
		return self.assignments

	def get_password():
		return self.password