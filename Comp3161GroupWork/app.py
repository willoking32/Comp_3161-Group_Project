from flask import Flask, render_template, request, redirect, session

import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Cur_User = [-1, ""]  # Initialize Cur_User as a global variable

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

def courseEnrollmentTable():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses_enrolment (
                    coursecode VARCHAR(21) PRIMARY KEY ,
                    name VARCHAR(100) NOT NULL,
                    lecturer_id INTEGER NOT NULL,
                    FOREIGN KEY (lecturer_id) REFERENCES users(id));''')
    conn.commit()
    conn.close()

# Endpoint for user registration
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        sid = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        gender = request.form.get('gender')
        stype = request.form.get('type')

        if not sid or not password or not firstname or not lastname or not gender or not stype:
            return render_template('register.html', error='ID, first name, last name, password, gender and type are required')

        # Check if id already exists
        conn = connect_to_mysql()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (sid,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error='ID already exists')

        cursor.execute("INSERT INTO users (id, firstname, lastname, password, gender,type) VALUES (%s, %s, %s, %s, %s,%s)", (sid, firstname, lastname, password, gender,stype))
        conn.commit()
        conn.close()

        return render_template('register.html', message='User registered successfully')
    else:
        return render_template('register.html')

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

        cursor.execute("SELECT id,type FROM users WHERE id = %s AND password = %s", (user_id, password))
        user = cursor.fetchone()

        conn.close()
        if user:
            session['user_id'] = user[0]
            session['type'] = user[1]
            Cur_User = [user_id, user[1]]  # Update Cur_User
            return render_template('create_course.html')    
        else:
            return render_template('login.html', error='Invalid ID or password')
    else:
        return render_template('login.html')

# Endpoint for user logout
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
        if Cur_User[1] == 'Admin':
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
    return render_template('create_course.html')

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
    cursor.execute("SELECT courses.* FROM courses INNER JOIN course_enrollment ON courses.id = course_enrollment.course_id WHERE course_enrollment.student_id = %s", (student_id,))
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

if __name__ == '__main__':
    create_users_table()
    create_courses_table()
    courseEnrollmentTable()
    app.run(debug=True)