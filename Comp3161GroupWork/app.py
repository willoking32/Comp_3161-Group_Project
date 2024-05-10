import hashlib
from flask import Flask, render_template, request, redirect, session,jsonify

import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Cur_User = [9, "Admin"]  # Initialize Cur_User as a global variable

def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="comp3161project"
    )

def create_users_table():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    firstname VARCHAR(255) NOT NULL,
                    lastname VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    gender VARCHAR(255) NOT NULL,
                    type VARCHAR(255) NOT NULL);''')
    conn.commit()
    conn.close()

def create_courses_table():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    coursecode VARCHAR(21) PRIMARY KEY ,
                    name VARCHAR(100) NOT NULL,
                    lecturer_id INTEGER NOT NULL,
                    FOREIGN KEY (lecturer_id) REFERENCES users(id));''')
    conn.commit()
    conn.close()

def courseEnrolmentTable():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS `course_enrolment`;""")
    cursor.execute('''CREATE TABLE IF NOT EXISTS course_enrolment (
                    student_id VARCHAR(100) NOT NULL,
                    course_title VARCHAR(100) NOT NULL,
                    coursecode VARCHAR(21) PRIMARY KEY ,
                    FOREIGN KEY (coursecode) REFERENCES users(id));''')
    conn.commit()
    conn.close()

# Endpoint for user registration
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    global Cur_User
    if request.method == 'POST':
        sid = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        gender = request.form.get('gender')
        stype = request.form.get('type')

        if not sid or not password or not firstname or not lastname or not gender or not stype:
            return render_template('register.html', error='ID, first name, last name, password, gender and type are required', Cur_User=Cur_User)

        # Check if id already exists
        conn = connect_to_mysql()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (sid,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error='ID already exists', Cur_User=Cur_User)

        cursor.execute("INSERT INTO users (id, firstname, lastname, password, gender, type) VALUES (%s, %s, %s, %s, %s, %s)", (sid, firstname, lastname, password, gender, stype))
        conn.commit()
        conn.close()

        return render_template('register_user.html', message='User registered successfully', Cur_User=Cur_User)
    else:
        return render_template('register_user.html', Cur_User=Cur_User)

@app.route('/')
def header():
    return render_template('header.html', Cur_User=Cur_User)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global Cur_User
    if request.method == 'POST':
        user_id = request.form.get('id')
        password = request.form.get('password')

        if not user_id or not password:
            return render_template('login.html', error='ID and password are required')

        conn = connect_to_mysql()
        cursor = conn.cursor()

        cursor.execute("SELECT id, type, password FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        conn.close()
        if user and user[2] == password:
            session['user_id'] = user[0]
            session['type'] = user[1]
            Cur_User = [user_id, user[1]]  # Update Cur_User
            if user[1]=="Admin":
                return redirect('/courses')
            elif user[1] == "Lecturer":
                return redirect(f'/courses/student/{user[0]}')
            elif user[1]== "Student":
                return redirect(f'/courses/lecturer/{user[0]}')    
        else:
            return render_template('login.html', error='Invalid ID or password')
    else:
        return render_template('login.html', Cur_User=Cur_User)

@app.route('/logout')
def logout():
    global Cur_User
    Cur_User = [-1, ""]  # Reset Cur_User
    session.clear()
    return redirect('/login')

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    global Cur_User
    if request.method == 'POST':
        if Cur_User and Cur_User[1] == 'Admin':
            course_name = request.form.get('course_name')
            coursecode = request.form.get('course_ID')
            lecturer_id = request.form.get('assigned_lecturer_id')

            if not course_name or not coursecode or not lecturer_id:
                return render_template('create_course.html', error='Course name, course ID, and assigned lecturer are required')

            conn = connect_to_mysql()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO courses (name, coursecode, lecturer_id) VALUES (%s, %s, %s)", (course_name, coursecode, lecturer_id))
            conn.commit()
            conn.close()

            return redirect('/courses')  # Redirect to courses page after course creation
        else:
            return render_template('create_course.html', error='Not Authorized')
    return render_template('create_course.html', Cur_User=Cur_User)

@app.route('/courses')
def all_courses():
    global Cur_User
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return render_template('courses.html', courses=courses, Cur_User=Cur_User)

@app.route('/courses/student/<int:student_id>')
def student_courses(student_id):
    global Cur_User
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT courses.* FROM courses INNER JOIN course_enrolment ON courses.coursecode = course_enrolment.coursecode WHERE course_enrolment.student_id = %s", (student_id,))
    courses = cursor.fetchall()
    conn.close()
    return render_template('courses.html', courses=courses, Cur_User=Cur_User)

@app.route('/courses/lecturer/<int:lecturer_id>')
def lecturer_courses(lecturer_id):
    global Cur_User
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE lecturer_id = %s", (lecturer_id,))
    courses = cursor.fetchall()
    conn.close()
    return render_template('courses.html', courses=courses, Cur_User=Cur_User)

@app.route('/courses/register', methods=['GET','POST'])
def register_course():
    global Cur_User
    if request.method=='POST':
        # Check if user is logged in
        if 'user_id' not in session:
            return render_template('error.html', error='Unauthorized', Cur_User=Cur_User), 401

        # Check if user is a student
        if session.get('type') != 'Student':
            return render_template('error.html', error='Only students can register for courses', Cur_User=Cur_User), 403

        # Get courseId from request body
        course_id = request.form.get('courseId')
        course_title=request.form.get('courseTitle')
        # Check if courseId is provided
        if not course_id:
            return render_template('error.html', error='Course ID is required', Cur_User=Cur_User), 400

        # Check if the course exists
        conn = connect_to_mysql()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE coursecode = %s", (course_id,))
        course = cursor.fetchone()
        conn.close()

        if not course:
            return render_template('error.html', error='Course not found', Cur_User=Cur_User), 404

        # Register student for the course
        student_id = session['user_id']
        conn = connect_to_mysql()
        cursor = conn.cursor()

        # Check if the student is already registered for the course
        cursor.execute("SELECT * FROM course_enrolment WHERE student_id = %s AND coursecode = %s", (student_id, course_id))
        if cursor.fetchone():
            conn.close()
            return render_template('error.html', error='Student is already registered for this course', Cur_User=Cur_User), 400

        cursor.execute("INSERT INTO course_enrolment (student_id,course_title, coursecode) VALUES (%s, %s,%s)", (student_id,course_title, course_id))
        conn.commit()
        conn.close()

        return render_template('success.html', message='Student registered successfully', Cur_User=Cur_User)
    else:
        return render_template('register_course.html', Cur_User=Cur_User)

@app.route('/courses/members', methods=['GET', 'POST'])
def course_members():
    global Cur_User
    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/login')

        # Check if the user is authorized to view members
        if session.get('type') not in ['Lecturer', 'Admin']:
            return render_template('error.html', error='Unauthorized')

        conn = connect_to_mysql()
        cursor = conn.cursor(dictionary=True)
        course_code=request.form.get('course_code')
        # Get course details
        cursor.execute("SELECT * FROM courses WHERE coursecode = %s", (course_code,))
        course = cursor.fetchone()

        if not course:
            conn.close()
            return render_template('error.html', error='Course not found')

        # Get members of the course
        cursor.execute("SELECT users.id, users.firstname, users.lastname, users.gender, users.type FROM users JOIN course_enrollment ON users.id = course_enrollment.student_id WHERE course_enrollment.coursecode = %s", (course_code,))
        members = cursor.fetchall()

        conn.close()

        return render_template('course_members.html', course=course, members=members, Cur_User=Cur_User)
    else:
        return render_template('getcourse.html', Cur_User=Cur_User)

if __name__ == '__main__':
    create_users_table()
    create_courses_table()
    courseEnrolmentTable()
    app.run(debug=True)