from flask import Flask, jsonify, request, make_response
import mysql.connector


app = Flask(__name__)




@app.route('/register', methods=['POST'])
def register_user():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE")

        cursor = cnx.cursor()
        data = request.get_json()
        user_id = data.get('user_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        user_type = data.get('user_type')
        cursor.execute(f"INSERT INTO Users VALUES('{user_id}','{first_name}','{last_name}','{password}','{user_type}')")


        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success" : "Costomer added"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)




@app.route('/login', methods=['POST'])
def user_login():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE")

        cursor = cnx.cursor()

        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        cursor.execute(f"SELECT Password, UserType from Users WHERE UserID = {user_id}")
        result = cursor.fetchone()

        cursor.close()
        cnx.close()
        

        if result[0] == password:
            return jsonify({'message': 'Login successful', 'user_type': result[1]}), 200
        else:
            return make_response("Login Failed", 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/courses', methods=['POST'])
def create_course():
    try:
        if not request.headers.get('X-User-Type') == 'admin':
            return make_response("Unauthorized", 403)
        
        data = request.get_json()
        course_id = data.get('course_id')
        course_name = data.get('course_name')
        lecturer_id = data.get('lecturer_id')


        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute(f"INSERT INTO Courses VALUES('{course_id}','{course_name}','{lecturer_id}')")

        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success": "Course created"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    

@app.route('/courses/<user_id>', methods=['GET'])
def get_courses(user_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()

        if user_id == "None":
            cursor.execute("SELECT * FROM Courses")
        else:
            query = f"""SELECT Courses.CourseID, Courses.CourseName, Courses.LecturerID FROM Courses 
                        LEFT JOIN Enrollments ON Courses.CourseID = Enrollments.CourseID
                        LEFT JOIN Users ON Courses.LecturerID = Users.UserID 
                        WHERE Enrollments.StudentID = '{user_id}' OR Courses.LecturerID = '{user_id}'"""

            cursor.execute(query)
        result = cursor.fetchall()
        course_list = []
        for course_code , course_name , course_description  in result:
            courses = {}
            courses['course_code'] = course_code
            courses['course_name'] = course_name
            courses['course_description'] = course_description
            course_list.append(courses)

        cursor.close()
        cnx.close()
        return make_response(course_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    

@app.route('/register_course', methods=['POST'])
def register_for_course():
    try:
        data = request.get_json()
        enroll_id = data.get('enroll_id')
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        user_type = data.get('user_type')

        if user_type not in ['student', 'lecturer']:
            return make_response("Invalid user type", 400)
        
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()


        if user_type == 'lecturer':
            cursor.execute(f"UPDATE Courses SET LecturerID = '{user_id}' WHERE CourseID = '{course_id}'")
        else:
            cursor.execute(f"INSERT INTO Enrollments VALUES('{enroll_id}', '{user_id}', '{course_id}')")
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success": "Registration successful"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)




@app.route('/course_members/<course_id>', methods=['GET'])
def get_course_members(course_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("SELECT Enrollments.StudentID, Users.FirstName, Users.LastName FROM Enrollments JOIN Users ON Enrollments.StudentID = Users.UserID WHERE CourseID = %s", (course_id,))

        members_list = []
        result = cursor.fetchall()
        for StudentID , FirstName, LastName in result:
            members = {}
            members['student_id'] = StudentID
            members['firstName'] = FirstName
            members['lastName'] = LastName
            members_list.append(members)

        cursor.close()
        cnx.close()
        return make_response(members_list, 200)
    
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    

@app.route('/calendar_events', methods=['POST'])
def create_calendar_event():
    try:
        data = request.get_json()
        event_id = data.get('event_id')
        course_id = data.get('course_id')
        event_date = data.get('event_date')
        event_discription = data.get('event_discription')
        
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO CalendarEvents (EventID, CourseID, EventDate, EventDescription) VALUES (%s, %s, %s, %s)", (event_id, course_id, event_date, event_discription))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success": "Event created"}, 201)
    
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/calendar_events/<course_id>', methods=['GET'])
def get_calendar_events(course_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()

        cursor.execute("SELECT CourseID, EventDate, EventDescription FROM CalendarEvents WHERE CourseID = %s", (course_id,))
        event_list = []
        result = cursor.fetchall()
        for CourseID, EventDate, EventDescription in result:
            events = {}
            events['course_id'] = CourseID
            events['event_date'] = EventDate
            events['event_description'] = EventDescription
            event_list.append(events)
        cursor.close()
        cnx.close()
        return jsonify(event_list)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    

# @app.route('/calendar_events/course/<course_id>', methods=['GET'])
# def get_calendar_events_for_course(course_id):
#     try:
#         cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
#         cursor = cnx.cursor()

#         # SQL to retrieve all events for a particular course
#         cursor.execute("SELECT event_id, title, event_date FROM calendar_events WHERE course_id = %s", (course_id,))
#         events = cursor.fetchall()

#         # Convert fetched data into a list of dictionaries
#         event_list = [{'event_id': event[0], 'title': event[1], 'date': event[2]} for event in events]

#         cursor.close()
#         cnx.close()
#         return jsonify(event_list)
#     except Exception as e:
#         return make_response({'error': str(e)}, 400)


@app.route('/calendar_events/student/<student_id>/date/<date>', methods=['GET'])
def get_calendar_events_for_student_on_date(student_id, date):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()

        # SQL to retrieve all events for a particular student on a specific date
        # Assuming 'student_course_registrations' relates students with courses
        cursor.execute("""
            SELECT ce.CourseID, ce.EventDate, ce.EventDescription
            FROM CalendarEvents ce
            JOIN Enrollments en ON ce.CourseID = en.CourseID
            WHERE en.StudentID = %s AND ce.EventDate = %s
        """, (student_id, date))

        event_list = []
        result = cursor.fetchall()
        for CourseID, EventDate, EventDescription in result:
            events = {}
            events['course_id'] = CourseID
            events['event_date'] = EventDate
            events['event_description'] = EventDescription
            event_list.append(events)

        cursor.close()
        cnx.close()
        return jsonify(event_list)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    


@app.route('/forums/<course_id>', methods=['GET'])
def get_forums(course_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("SELECT ForumID, CourseID, ForumName FROM Forums WHERE CourseID = %s", (course_id,))

        forums_list = []
        result = cursor.fetchall()
        for ForumID, CourseID, ForumName in result:
            forums = {}
            forums['course_id'] = ForumID
            forums['event_date'] = CourseID
            forums['event_description'] = ForumName
            forums_list.append(forums)
        cursor.close()
        cnx.close()
        return jsonify(forums_list)
    except Exception as e:
        return make_response({'error': str(e)}, 400)



@app.route('/forums', methods=['POST'])
def create_forum():
    try:
        data = request.get_json()
        forum_id = data['forum_id']
        course_id = data['course_id']
        forum_name = data['forum_name']

        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO Forums (ForumID, CourseID, ForumName) VALUES (%s, %s, %s)", (forum_id, course_id, forum_name))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"success": "Forum created"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    


@app.route('/threads/<forum_id>', methods=['GET'])
def get_threads(forum_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("SELECT ThreadID, ForumID, UserID, ThreadTitle, ThreadPost, ParentThreadID FROM DiscussionThreads WHERE ForumID = %s", (forum_id,))
        threads_list = []
        result = cursor.fetchall()
        for ThreadID, ForumID, UserID, ThreadTitle, ThreadPost, ParentThreadID in result:
            threads = {}
            threads['thread_id'] = ThreadID
            threads['forum_id'] = ForumID
            threads['user_id'] = UserID
            threads['thread_title'] = ThreadTitle
            threads['thread_post'] = ThreadPost
            threads['parent_thread_id'] = ParentThreadID
            threads_list.append(threads)

        cursor.close()
        cnx.close()
        return jsonify(threads_list)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/threads', methods=['POST'])
def add_thread():
    try:
        data = request.get_json()
        thread_id = data['thread_id']
        forum_id = data['forum_id']
        user_id = data['user_id']
        thread_title = data['thread_title']
        thread_post = data['thread_post']
        parent_thread_id = data.get('parent_thread_id')


        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO DiscussionThreads (ThreadID, ForumID, UserID, ThreadTitle, ThreadPost, ParentThreadID) VALUES (%s, %s, %s, %s, %s, %s)", (thread_id, forum_id, user_id, thread_title, thread_post, parent_thread_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"success": "Thread added"}), 201
    
    except Exception as e:
        return make_response({'error': str(e)}, 400)



@app.route('/content', methods=['POST'])
def add_content():
    try:
        if not request.headers.get('X-User-Type') == 'lecturer':
            return make_response("Unauthorized", 403)


        data = request.get_json()
        content_id = data['content_id']
        course_id = data['course_id']
        lecturer_id = data['lecturer_id']
        content_type = data['content_type']
        content_description = data['content_description']
        section_name = data['section_name']



        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO CourseContent (ContentID, CourseID, LecturerID, ContentType, ContentDescription, SectionName) VALUES (%s, %s, %s, %s, %s, %s)", (content_id, course_id, lecturer_id, content_type, content_description, section_name))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"success": "Content added"}), 201
    
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/content/<course_id>', methods=['GET'])
def get_content(course_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("SELECT ContentID, CourseID, LecturerID, ContentType, ContentDescription, SectionName FROM CourseContent WHERE CourseID = %s", (course_id,))
        content_list = []
        result = cursor.fetchall()
        for ThreadID, ForumID, UserID, ThreadTitle, ThreadPost, ParentThreadID in result:
            content = {}
            content['thread_id'] = ThreadID
            content['forum_id'] = ForumID
            content['user_id'] = UserID
            content['thread_title'] = ThreadTitle
            content['thread_post'] = ThreadPost
            content['parent_thread_id'] = ParentThreadID
            content_list.append(content)
        cursor.close()
        cnx.close()
        return jsonify(content_list)
    except Exception as e:
        return make_response({'error': str(e)}, 400)





@app.route('/assignments', methods=['POST'])
def submit_assignment():
    try:

        if not request.headers.get('X-User-Type') == 'student':
            return make_response("Unauthorized", 403)
        
        data = request.get_json()

        assignment_id = data['assignment_id']
        course_id = data['course_id']
        student_id = data['student_id']
        assignment_name = data['assignment_name']



        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO assignments (AssignmentID, CourseID, StudentID, AssignmentName) VALUES (%s, %s, %s, %s)", (assignment_id, course_id, student_id, assignment_name))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"success": "Assignment submitted"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    



@app.route('/assignments/grade', methods=['POST'])
def update_assignment_grade():
    try:

        if not request.headers.get('X-User-Type') == 'lecturer':
            return make_response("Unauthorized", 403)
        
        data = request.get_json()

        assignment_id = data['assignment_id']
        course_id = data['course_id']
        student_id = data['student_id']
        grade = data['grade']



        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("UPDATE Assignments SET Grade = %s WHERE CourseID = %s AND StudentID = %s AND AssignmentID = %s", (grade, course_id, student_id, assignment_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"success": "Grade submitted"}), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    


@app.route('/student/final_Grade/<student_id>', methods=['GET'])
def get_student_final_grade(student_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute("SELECT StudentID, AVG(Grade) FROM Assignments WHERE StudentID = %s", (student_id,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return jsonify({"student_id":result[0], "final_grade": result[1]})
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    



    

def retrieve_report_data(view_name):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor(dictionary=True)  # Use dictionary cursor to directly fetch row headers with data
        cursor.execute(f"SELECT * FROM {view_name}")
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return jsonify(results)  # Use jsonify to convert the list of dictionaries to a JSON response
    except Exception as e:
        return make_response({'error': str(e)}, 400)





@app.route('/report/courses_with_50_students', methods=['GET'])
def get_courses_with_50_students():
    return retrieve_report_data('CoursesWithFiftyOrMoreStudents')

@app.route('/report/students_with_5_courses', methods=['GET'])
def get_students_with_5_courses():
    return retrieve_report_data('StudentsWithFiveOrMoreCourses')

@app.route('/report/lecturers_with_3_courses', methods=['GET'])
def get_lecturers_with_3_courses():
    return retrieve_report_data('LecturersWithThreeOrMoreCourses')

@app.route('/report/top_10_enrolled_courses', methods=['GET'])
def get_top_10_enrolled_courses():
    return retrieve_report_data('TopTenEnrolledCourses')

@app.route('/report/top_10_students_by_average', methods=['GET'])
def get_top_10_students_by_average():
    return retrieve_report_data('TopTenStudentsHighestAverages')

def retrieve_report_data(view_name):
    try:
      
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="OURVLE_CLONE")
        cursor = cnx.cursor()
        cursor.execute(f"SELECT * FROM {view_name}")
        results = [{'id': row[0], 'value': row[1]} for row in cursor.fetchall()]
        cursor.close()
        cnx.close()
        return jsonify(results)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    








@app.route('/customers', methods=['GET'])
def get_customerinfo():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE"
)
        cursor = cnx.cursor()
        cursor.execute('SELECT * from customerinfo')
        customerinfo_list = []
        for CustomerID, Gender, Age, Annual_Income, Spending_Score, Profession,Work_Experience, Family_Size  in cursor:
            customerinfo = {}
            customerinfo['id'] = CustomerID
            customerinfo['gender'] = Gender
            customerinfo['age'] = Age
            customerinfo['annual_income'] = Annual_Income
            customerinfo['spending_score'] = Spending_Score
            customerinfo['profession'] = Profession
            customerinfo['work_experience'] = Work_Experience
            customerinfo['family_size'] = Family_Size
            customerinfo_list.append(customerinfo)
        cursor.close()
        cnx.close()
        return make_response(customerinfo_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/customer/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE"
)
        cursor = cnx.cursor()
        cursor.execute(f"SELECT * from customerinfo WHERE CustomerID={customer_id}")
        row = cursor.fetchone()
        customerinfo_list = []      
        if row is not None:
            CustomerID, Gender, Age, Annual_Income, Spending_Score, Profession,Work_Experience, Family_Size  = row
            customerinfo = {}
            customerinfo['id'] = CustomerID
            customerinfo['gender'] = Gender
            customerinfo['age'] = Age
            customerinfo['annual_income'] = Annual_Income
            customerinfo['spending_score'] = Spending_Score
            customerinfo['profession'] = Profession
            customerinfo['work_experience'] = Work_Experience
            customerinfo['family_size'] = Family_Size
            cursor.close()
            cnx.close()
            return make_response(customerinfo, 200)
        else:
            return make_response({'error': 'Customer not found'}, 400)
    except Exception as e:
        print(e)  
        return make_response({'error': 'An error has occurred'}, 500)

@app.route('/add_customer', methods=['POST'])
def add_student():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE")

        cursor = cnx.cursor()
        content = request.json
        CustomerID = content.get('CustomerID')
        Gender = content.get('Gender')
        Age = content.get('Age')
        Annual_Income = content.get('Annual_Income')
        Spending_Score = content.get('Spending_Score')
        Profession = content.get('Profession')
        Work_Experience = content.get('Work_Experience')
        Family_Size = content.get('Family_Size')
        cursor.execute(f"INSERT INTO customerinfo VALUES('{CustomerID}','{Gender}','{Age}','{Annual_Income}','{Spending_Score}','{Profession}','{Work_Experience}','{Family_Size}')")



        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success" : "Costomer added"}, 201)
    
    except Exception as e:
        print(e)
        return make_response({'error': 'An error has occured'}, 400)

@app.route('/update_profession/<customer_id>', methods=['PUT'])
def update_profession(customer_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE")

        cursor = cnx.cursor()
        content = request.json
        Profession = content['Profession']
        cursor.execute(f"UPDATE customerinfo SET Profession='{Profession}' WHERE CustomerID={customer_id}")
        cnx.commit()
        cursor.close()
        return make_response({"success" : "Customer updated"}, 202)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/delete_student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                            host='127.0.0.1',
                                            database='uwi')
        cursor = cnx.cursor()
        cursor.execute(f"DELETE FROM Students WHERE StudentID={student_id}")
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success" : "Student deleted"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/address_report', methods=['GET'])
def get_addresses():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                            host='127.0.0.1',
                                            database='uwi')
        cursor = cnx.cursor()
        cursor.execute(f"SELECT * FROM ALL_ADRESSESS")
        address_lst = []
        for add in cursor:
            address = {}
            address['Address'] = add[0]
            address_lst.append(address)
        return make_response(address_lst, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
@app.route('/highest_income_report', methods=['GET'])
def get_highest_income():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE"
)
        cursor = cnx.cursor()
        cursor.execute(f"""
        SELECT ci1.CustomerID, ci1.Annual_Income AS AnnualIncome, ci1.Profession
        FROM customerinfo ci1
        JOIN (
            SELECT Profession, MAX(Annual_Income) AS MaxIncome
            FROM customerinfo
            GROUP BY Profession
        ) ci2 ON ci1.Profession = ci2.Profession AND ci1.Annual_Income = ci2.MaxIncome
        ORDER BY ci1.Annual_Income DESC;
        """)

        customerinfo_list = []
        for CustomerID, Annual_Income, Profession in cursor:
            customerinfo = {}
            customerinfo['id'] = CustomerID
            customerinfo['annual_income'] = Annual_Income
            customerinfo['profession'] = Profession
            customerinfo_list.append(customerinfo)
  
        cursor.close()
        cnx.close()
        return make_response(customerinfo_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    

@app.route('/total_income_report', methods=['GET'])
def total_income():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE"
)
        cursor = cnx.cursor()
        cursor.execute(f"""
        SELECT SUM(Annual_Income) AS TotalIncome, Profession
        FROM customerinfo
        GROUP BY Profession
        ORDER BY TotalIncome DESC;
        """)

        customerinfo_list = []
        for TotalIncome, Profession in cursor:
            customerinfo = {}
            customerinfo['TotalIncome'] = TotalIncome
            customerinfo['profession'] = Profession
            customerinfo_list.append(customerinfo)
  
        cursor.close()
        cnx.close()
        return make_response(customerinfo_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)




@app.route('/average_work_experience', methods=['GET'])
def average_work_experience():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE"
)
        cursor = cnx.cursor()
        cursor.execute(f"""
        SELECT Profession, AVG(Work_Experience) AS AverageWorkExperience
        FROM customerinfo
        WHERE Annual_Income > 50000 AND Age < 35
        GROUP BY Profession
        ORDER BY AverageWorkExperience DESC;
        """)

        customerinfo_list = []
        for Profession, AverageWorkExperience in cursor:
            customerinfo = {}
            customerinfo['profession'] = Profession
            customerinfo['AverageWorkExperience'] =int(AverageWorkExperience)
            customerinfo_list.append(customerinfo)
  
        cursor.close()
        cnx.close()
        return make_response(customerinfo_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)



@app.route('/average_spending_score/<profession>', methods=['GET'])
def average_spending_score(profession):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="OURVLE_CLONE"
)
        cursor = cnx.cursor()
        cursor.execute(f"""
        SELECT Gender, AVG(Spending_Score) AS AverageSpendingScore
        FROM customerinfo
        WHERE Profession = '{profession}'
        GROUP BY Gender
        ORDER BY AVG(Spending_Score) DESC;
        """)

        customerinfo_list = []
        for Gender, AverageSpendingScore in cursor:
            customerinfo = {}
            customerinfo['Gender'] = Gender
            customerinfo['AverageSpendingScore'] =int(AverageSpendingScore)
            customerinfo_list.append(customerinfo)
  
        cursor.close()
        cnx.close()
        return make_response(customerinfo_list, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
if __name__ == '__main__':
    app.run(port=6000)