import random
from faker import Faker
import mysql.connector


fake = Faker()


connection = mysql.connector.connect(
    host="localhostt",
    user="root",
    password="DoveLove",
    database="OURVLE_CLONE"
)


def execute_query(query, values=None):
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()


def generate_users(num_users):
    users = []
    for i in range(num_users):
        user = {
            'UserID': i + 1,
            'Username': fake.user_name(),
            'Password': fake.password(),
            'UserType': random.choice(['admin', 'lecturer', 'student'])
        }
        users.append(user)
    return users


def generate_courses(num_courses, num_lecturers):
    courses = []
    for i in range(num_courses):
        course = {
            'CourseID': i + 1,
            'CourseName': fake.catch_phrase(),
            'LecturerID': random.randint(1, num_lecturers)
        }
        courses.append(course)
    return courses


num_users = 100000
num_courses = 200
num_lecturers = 50
num_students = 100000
num_events = 500
num_forums = 100
num_threads = 1000
num_content = 500
num_assignments = 1000
num_enrollments = 50000


users = generate_users(num_users)
courses = generate_courses(num_courses, num_lecturers)


for user in users:
    query = "INSERT INTO Users (UserID, Username, Password, UserType) VALUES (%s, %s, %s, %s)"
    values = (user['UserID'], user['Username'], user['Password'], user['UserType'])
    execute_query(query, values)


for course in courses:
    query = "INSERT INTO Courses (CourseID, CourseName, LecturerID) VALUES (%s, %s, %s)"
    values = (course['CourseID'], course['CourseName'], course['LecturerID'])
    execute_query(query, values)


for enrollment in enrollments:
    query = "INSERT INTO Enrollments (EnrollmentID, StudentID, CourseID) VALUES (%s, %s, %s)"
    values = (enrollment['EnrollmentID'], enrollment['StudentID'], enrollment['CourseID'])
    execute_query(query, values)


for event in calendar_events:
    query = "INSERT INTO CalendarEvents (EventID, CourseID, EventDate, EventDescription) VALUES (%s, %s, %s, %s)"
    values = (event['EventID'], event['CourseID'], event['EventDate'], event['EventDescription'])
    execute_query(query, values)


for forum in forums:
    query = "INSERT INTO Forums (ForumID, CourseID, ForumName) VALUES (%s, %s, %s)"
    values = (forum['ForumID'], forum['CourseID'], forum['ForumName'])
    execute_query(query, values)


for thread in discussion_threads:
    query = "INSERT INTO DiscussionThreads (ThreadID, ForumID, UserID, ThreadTitle, ThreadPost, ParentThreadID) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (thread['ThreadID'], thread['ForumID'], thread['UserID'], thread['ThreadTitle'], thread['ThreadPost'], thread['ParentThreadID'])
    execute_query(query, values)


for content_item in course_content:
    query = "INSERT INTO CourseContent (ContentID, CourseID, LecturerID, ContentType, ContentDescription, SectionName) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (content_item['ContentID'], content_item['CourseID'], content_item['LecturerID'], content_item['ContentType'], content_item['ContentDescription'], content_item['SectionName'])
    execute_query(query, values)


for assignment in assignments:
    query = "INSERT INTO Assignments (AssignmentID, CourseID, StudentID, AssignmentName, Grade) VALUES (%s, %s, %s, %s, %s)"
    values = (assignment['AssignmentID'], assignment['CourseID'], assignment['StudentID'], assignment['AssignmentName'], assignment['Grade'])
    execute_query(query, values)

connection.close()
