import pytest
import System

#Tests if the program can handle a wrong username
def test_login(grading_system):
    username = 'thtrhg'
    password =  'fhjhjdhjdfh'
    grading_system.login(username,password)


@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem

import Student
username = 'pwddd'
password =  '#pordy'
username2 = 'hdddd'
username3 = 'yk3321'
course = 'software engineering'
assignment = 'assignment1'
profUser = 'goggins'
profPass = 'augurrox'
#pass
def test_login(grading_system):
    users = grading_system.users
    grading_system.login(username,password)
    grading_system.__init__()
    if users[username]['role'] != 'professor':
        assert False
#pass
def test_check_password(grading_system):
    test = grading_system.check_password(username,password)
    test2 = grading_system.check_password(username,'#yeet')
    test3 = grading_system.check_password(username,'#YEET')
    if test == test3 or test2 == test3:
        assert False
    if test != test2:
        assert False
