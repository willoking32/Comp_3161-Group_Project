from flask import Flask, jsonify, request, make_response
import mysql.connector


app = Flask(__name__)




@app.route('/register', methods=['POST'])
def register_user():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3")

        cursor = cnx.cursor()
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        user_type = data.get('user_type')
        cursor.execute(f"INSERT INTO customerinfo VALUES('{user_id}','{password}','{user_type}')")


        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success" : "Costomer added"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)




@app.route('/login', methods=['POST'])
def user_login():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3")

        cursor = cnx.cursor()

        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        cursor.execute(f"SELECT password , user_type from customerinfo where user_id = {user_id}")

        




        cursor.close()
        cnx.close()

        if cursor[0] == password:
            return jsonify({'message': 'Login successful', 'user_type': cursor[1]}), 200
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
        course_code = data.get('course_code')
        course_name = data.get('course_name')
        course_description = data.get('course_description')


        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="lab3")
        cursor = cnx.cursor()
        cursor.execute(f"INSERT INTO customerinfo VALUES('{course_code}','{course_name}','{course_description}')")

        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success": "Course created"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    

@app.route('/courses/<user_id>', methods=['GET'])
def get_courses(user_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="lab3")
        cursor = cnx.cursor()

        if user_id == None:
            cursor.execute("SELECT * FROM courses")
        else:
            cursor.execute(f"SELECT * FROM courses WHERE lecturer_id = '{user_id} OR Student_id = '{user_id}")

        course_list = []
        for course_code , course_name , course_description  in cursor:
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

    data = request.get_json()
    user_id = data.get('user_id')
    course_id = data.get('course_id')
    user_type = data.get('user_type')

    if user_type not in ['student', 'lecturer']:
        return make_response("Invalid user type", 400)
    
    cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="lab3")
    cursor = cnx.cursor()


    if user_type == 'lecturer':
        cursor.execute("INSERT INTO course_registrations (user_id, course_id, user_type) VALUES (%s, %s, %s)", (user_id, course_id, user_type))
    else:
        cursor.execute("INSERT INTO course_registrations (user_id, course_id, user_type) VALUES (%s, %s, %s)", (user_id, course_id, user_type))
    cnx.commit()
    cursor.close()
    cnx.close()
    return make_response({"success": "Registration successful"}, 201)




@app.route('/course_members/<course_id>', methods=['GET'])
def get_course_members(course_id):
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost", database="lab3")
        cursor = cnx.cursor()
        cursor.execute("SELECT user_id, user_type FROM course_registrations WHERE course_id = %s", (course_id,))

        course_list = []
        for user_id , user_type  in cursor:
            courses = {}
            courses['course_code'] = user_id
            courses['user_type'] = user_type
            course_list.append(courses)

        cursor.close()
        cnx.close()
        return make_response(course_list, 200)
    
    except Exception as e:
        return make_response({'error': str(e)}, 400)

























@app.route('/customers', methods=['GET'])
def get_customerinfo():
    try:
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3"
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
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3"
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
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3")

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
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3")

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
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3"
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
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3"
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
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3"
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
        cnx = mysql.connector.connect(user='root', password="islandwater", host="localhost" , database="lab3"
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