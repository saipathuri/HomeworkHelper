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
		self.date = beautiful_date(date)
		self.course = course

	def to_string():
		string = self.course + self.name + "due on " + beautiful_date(self.date)

	def beautiful_date(date_str):
		date = datetime.datetime.strptime(date_str.split("T")[0], "%Y-%m-%d").date()
		date_str = str(calendar.month_name[date.month])
		date_str += " " + str(date.day) + ", " + str(date.year)
		return date_str