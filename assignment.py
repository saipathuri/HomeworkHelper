from datetime import date
import datetime
import calendar

class assignment(object):
	def __init__(self):
		self.name = 'Assignment Name'
		self.due_date = date(2000,1,1)
		self.course = "CourseName"
		self.pretty_date = ""

	def set_name(self,name):
		self.name = name

	def get_name(self):
		return self.name

	def set_date(self, due_date):
		self.due_date = self.create_date_obj(due_date)
		self.pretty_date = self.beautiful_date(due_date)

	def get_date(self):
		return self.due_date

	def get_pretty_date(self):
		return self.pretty_date

	def set_course(self, course_name):
		self.course = course_name

	def get_course(self):
		return self.course

	def create_assignment(self, name, date, course):
		self.set_name(name)
		self.set_date(date)
		self.set_course(course)

	def to_string(self):
		string = str(self.course) + " " + str(self.name) + " due on " + str(self.pretty_date)
		return string

	def create_date_obj(self, date_str):
		return datetime.datetime.strptime(date_str.split("T")[0], "%Y-%m-%d").date()

	def beautiful_date(self, date_str):
		date_as_obj = self.create_date_obj(date_str)
		date_str = str(calendar.month_name[date_as_obj.month])
		date_str += " " + str(date_as_obj.day) + ", " + str(date_as_obj.year)
		return date_str