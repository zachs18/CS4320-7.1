import pytest
import json

import System
import Student

@pytest.fixture
def grading_system():
	gradingSystem = System.System()
	#gradingSystem.load_data() # this already happens in System.__init__
	return gradingSystem

#pass
def test_login(grading_system):
	with open("Data/users.json") as userfile:
		users = json.load(userfile)
		for username, userinfo in users.items():
			grading_system.login(username, userinfo['password'])
			if grading_system.usr.name != username:
				assert False, "grading_system.login({}) failed".format(repr(username))
#pass
def test_check_password(grading_system):
	with open("Data/users.json") as userfile:
		users = json.load(userfile)
		for username, userinfo in users.items():
			correct = grading_system.check_password(username, userinfo['password'])
			assert correct, "correct password deemed incorrect for user {}".format(username)

			space   = grading_system.check_password(username, userinfo['password'] + " ")
			assert not space, "incorrect (space-at-end) password deemed correct for user {}".format(username)

			if userinfo['password'] != userinfo['password'].upper():
				upper = grading_system.check_password(username, userinfo['password'].upper())
				assert not upper, "incorrect password (uppercase) deemed correct for user {}".format(username)

			if userinfo['password'] != userinfo['password'].lower():
				upper = grading_system.check_password(username, userinfo['password'].lower())
				assert not upper, "incorrect password (lowercase) deemed correct for user {}".format(username)

			if userinfo['password'] != "#yeet":
				wrong1  = grading_system.check_password(username, "#yeet")
				assert not wrong1, "incorrect password (\"#yeet\") deemed correct for user {}".format(username)

			if userinfo['password'] != "#YEET":
				wrong2  = grading_system.check_password(username, "#YEET")
				assert not wrong2, "incorrect password (\"#YEET\") deemed correct for user {}".format(username)

			if userinfo['password'] != '':
				empty = grading_system.check_password(username, "")
				assert not empty, "empty password deemed correct for user {}".format(username)

			nopwd   = grading_system.check_password(username, None)
			assert not nopwd, "None password deemed correct for user {}".format(username)

#fail
def test_change_grade(grading_system):
	course = 'software_engineering'
	assignment = 'assignment1'
	for username in ["yted91", "hdjsr7"]:
		original_grade = None
		with open("Data/users.json") as userfile:
			users = json.load(userfile)
			original_grade = users[username]['courses'][course][assignment]['grade']
		grading_system.login("goggins", "augurrox")
		grading_system.usr.change_grade(username, course, assignment, original_grade+1)
		with open("Data/users.json") as userfile:
			users = json.load(userfile)
			assert users[username]['courses'][course][assignment]['grade'] == original_grade+1, \
				"Grade not correctly changed or saved"

#pass
def test_create_assignment(grading_system):
	course = 'software_engineering'
	assignment = 'assignment1'
	due_date = "1/1/21"

	grading_system.login("goggins", "augurrox")
	grading_system.usr.create_assignment(assignment, due_date, course)
	with open("Data/courses.json") as coursefile:
		courses = json.load(coursefile)
		assert assignment in courses[course]['assignments'], "Assignment not added to course db"
		assert courses[course]['assignments'][assignment]["due_date"] == due_date, "Assignment added to course db with incorrect due_date"

#fail
def test_add_student(grading_system):
	user = "akend3"
	course = "software_engineering"

	grading_system.login("goggins", "augurrox")
	grading_system.usr.add_student(user, course)
	# note that add_student will corrupt the copy of the course db
	# stored in memory for grading_system.user
	# since add_student does not deep copy the assignments dict
	# but there isn't really an easy way to test for that here,
	# and this test fails anyway, so :shrug:
	with open("Data/users.json") as userfile:
		users = json.load(userfile)
		assert course in users[user]['courses'], \
			"Student not correctly added to course"

#pass
def test_drop_student(grading_system):
	user = "akend3"
	course = "databases"

	grading_system.login("goggins", "augurrox")
	grading_system.usr.drop_student(user, course)
	with open("Data/users.json") as userfile:
		users = json.load(userfile)
		assert course not in users[user]['courses'], \
			"Student not correctly dropped from course"

#pass
def test_submit_assignment(grading_system):
	user = "akend3"
	password = "123454321"
	course = "comp_sci"
	assignment_name = "assignment1"
	submission = "This is a test submission!"
	submission_date = "11/1/20"

	grading_system.login(user, password)
	grading_system.usr.submit_assignment(course, assignment_name, submission, submission_date)
	with open("Data/users.json") as userfile:
		users = json.load(userfile)

		assert assignment_name in users[user]['courses'][course], \
			"Assignment not submitted correctly (not in db)"

		assert submission == users[user]['courses'][course][assignment_name]['submission'], \
			"Assignment not submitted correctly (db != submission)"

		assert submission_date == users[user]['courses'][course][assignment_name]['submission_date'], \
			"Assignment not submitted correctly (db != submission_date)"

#fail
def test_check_ontime(grading_system):
	user = "akend3"
	password = "123454321"

	grading_system.login(user, password)

	assert grading_system.usr.check_ontime("11/1/20", "11/2/20"), \
		"Submission before due date marked not ontime"

	assert grading_system.usr.check_ontime("11/1/20", "11/1/20"), \
		"Submission on due date marked not ontime"

	assert not grading_system.usr.check_ontime("11/1/20", "10/29/20"), \
		"Submission after due date marked ontime"

username2 = 'hdddd'
username3 = 'yk3321'
profUser = 'goggins'
profPass = 'augurrox'
