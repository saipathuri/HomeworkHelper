import assignment

class user(object):

	def __init__(self):
		self.phone_number = "+15556667777"
		self.assignments = []
		self.password = ""
		self.session_counter = 0

	def initialize_user(self, phone_number, password):
		self.phone_number = phone_number
		self.password = password
		return self

	def add_assignment(self, assignment_to_add):
		self.assignments.append(assignment_to_add)
		self.assignments.sort(key=lambda r: r.get_date())

	def get_assignments(self):
		return self.assignments

	def get_password(self):
		return self.password

	def increment_session(self):
		self.session_counter += 1

	def get_session_id(self):
		return self.phone_number + str(self.session_counter)

	def get_phone_number(self):
		return self.phone_number