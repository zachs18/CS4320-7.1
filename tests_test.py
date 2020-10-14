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

username2 = 'hdddd'
username3 = 'yk3321'
profUser = 'goggins'
profPass = 'augurrox'
