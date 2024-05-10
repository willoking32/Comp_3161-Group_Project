import random
from faker import Faker
import mysql.connector

fake = Faker()

connection = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE")


def execute_query(query, values=None):
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()

def generate_users(num_students, num_lecturers):
    users = []
    lecturer_ids = random.sample(range(1, num_students + num_lecturers + 1), num_lecturers)
    student_ids = [i for i in range(1, num_students + 1)]
    for i in range(num_students + num_lecturers):
        user_type = 'student'
        if i + 1 in lecturer_ids:
            user_type = 'lecturer'
        if i + 1 <= num_students:
            user_id = student_ids.pop(0)
        else:
            user_id = i + 1 - num_students
        user = {
            'UserID': user_id,
            'FirstName': fake.first_name(),
            'LastName': fake.last_name(),
            'Password': fake.password(),
            'UserType': user_type
        }
        users.append(user)
    return users


def generate_courses(num_courses, num_lecturers):
    courses = []
    lecturer_ids = list(range(1, num_lecturers + 1))
    for i in range(num_courses):
        lecturer_id = random.choice(lecturer_ids)
        courses.append({
            'CourseID': i + 1,
            'CourseName': fake.catch_phrase(),
            'LecturerID': lecturer_id
        })
        if len(courses) % 10 == 0:
            lecturer_ids.remove(lecturer_id)
    return courses


def generate_enrollments(num_students, num_courses):
    enrollments = []
    for student_id in range(1, num_students + 1):
        num_courses_per_student = random.randint(3, 6)
        student_courses = random.sample(range(1, num_courses + 1), num_courses_per_student)
        for course_id in student_courses:
            enrollments.append({
                'StudentID': student_id,
                'CourseID': course_id
            })
    return enrollments

def generate_calendar_events(num_events, num_courses):
    events = []
    for i in range(num_events):
        event = {
            'EventID': i + 1,
            'CourseID': random.randint(1, num_courses),
            'EventDate': fake.date_this_decade(),
            'EventDescription': fake.text()
        }
        events.append(event)
    return events

def generate_forums(num_forums, num_courses):
    forums = []
    for i in range(num_forums):
        forum = {
            'ForumID': i + 1,
            'CourseID': random.randint(1, num_courses),
            'ForumName': fake.catch_phrase()
        }
        forums.append(forum)
    return forums

def generate_threads(num_threads, num_forums, num_users):
    threads = []
    for i in range(num_threads):
        thread = {
            'ThreadID': i + 1,
            'ForumID': random.randint(1, num_forums),
            'UserID': random.randint(1, num_users),
            'ThreadTitle': fake.sentence(),
            'ThreadPost': fake.text(),
            'ParentThreadID': None  # Assuming no parent thread for initial threads
        }
        threads.append(thread)
    return threads

def generate_course_content(num_content, num_courses, num_lecturers):
    content = []
    for i in range(num_content):
        item = {
            'ContentID': i + 1,
            'CourseID': random.randint(1, num_courses),
            'LecturerID': random.randint(1, num_lecturers),
            'ContentType': random.choice(['link', 'file', 'slides']),
            'ContentDescription': fake.text(),
            'SectionName': fake.word()
        }
        content.append(item)
    return content

def generate_assignments(num_assignments, num_courses, num_students):
    assignments = []
    for i in range(num_assignments):
        assignment = {
            'AssignmentID': i + 1,
            'CourseID': random.randint(1, num_courses),
            'StudentID': random.randint(1, num_students),
            'AssignmentName': fake.catch_phrase(),
            'Grade': round(random.uniform(0, 100), 2)
        }
        assignments.append(assignment)
    return assignments

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

users = generate_users(num_students, num_lecturers)
courses = generate_courses(num_courses, num_lecturers)
enrollments = generate_enrollments(num_students, num_courses,num_lecturers)
calendar_events = generate_calendar_events(num_events, num_courses)
forums = generate_forums(num_forums, num_courses)
discussion_threads = generate_threads(num_threads, num_forums, num_users)
course_content = generate_course_content(num_content, num_courses, num_lecturers)
assignments = generate_assignments(num_assignments, num_courses, num_students)

for user in users:
    query = "INSERT INTO Users (UserID, FirstName, LastName, Password, UserType) VALUES (%s, %s, %s, %s, %s)"
    values = (user['UserID'], user['FirstName'], user['LastName'], user['Password'], user['UserType'])
    execute_query(query, values)

for course in courses:
    query = "INSERT INTO Courses (CourseID, CourseName, LecturerID) VALUES (%s, %s, %s)"
    values = (course['CourseID'], course['CourseName'], course['LecturerID'])
    execute_query(query, values)

for enrollment in enrollments:
    query = "INSERT INTO Enrollments (StudentID, CourseID) VALUES (%s, %s)"
    values = (enrollment['StudentID'], enrollment['CourseID'])
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