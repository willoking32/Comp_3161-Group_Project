from flask import Flask, render_template, request,redirect,session

import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Cur_User=""
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
    #cursor.execute('''DROP TABLE IF EXISTS `users`;''')
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
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    lecturer_id INTEGER NOT NULL,
                    FOREIGN KEY (lecturer_id) REFERENCES users(id));''')
    conn.commit()
    conn.close()

# Endpoint for user registration
@app.route('/register', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        sid = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        gender = request.form.get('gender')
        stype = request.form.get('type')

        if not sid or not password or not firstname or not lastname or not gender or not stype:
            return render_template('register.html', error='ID, first name, last name, password,  gender and type are required')

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

@app.route('/login', methods=['GET', 'POST'])
def login():
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
            return render_template('create_course.html')    
        else:
            return render_template('login.html', error='Invalid ID or password')
    else:
        return render_template('login.html')

# Endpoint for user logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    

    if request.method == 'POST':
        
        course_name = request.form.get('course_name')
        lecturer_id = session['user_id']

        if not course_name:
            return render_template('create_course.html', error='Course name is required')

        conn = connect_to_mysql()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO courses (name, lecturer_id) VALUES (%s, %s)", (course_name, lecturer_id))
        conn.commit()
        conn.close()

        return redirect('/logout')    
    else:
        return render_template('login.html')
    

    
    
if __name__ == '__main__':
    create_users_table()
    create_courses_table()
    app.run(debug=True)