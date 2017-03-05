import assignment

class user(object):

	def __init__(self):
		self.phone_number = "+15556667777"
		self.assignments = []
		self.password = ""

	def initialize_user(self, phone_number, password):
		self.phone_number = phone_number
		self.password = password
		return self

	def add_assignment(self, assignment_to_add):
		self.assignments.append(assignment_to_add)

	def get_assignments(self):
		return self.assignments

	def get_password(self):
		return self.password