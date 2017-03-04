from datetime import date

class assignment(object):
	def __init__(self):
		self.name = 'Assignment Name'
		self.date = date(2000,1,1)
		self.course = "CourseName"

	def set_name(name):
		self.name = name

	def set_date(due_date):
		if isinstance(due_date, date):
			self.date = due_date
		else:
			raise TypeError("Requires datetime.date")

	def set_course(course_name):
		self.course = course_name

	def create_assignment(name, date, course):
		self.name = name
		self.date = date
		self.course = course