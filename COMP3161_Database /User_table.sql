CREATE TABLE User_table (
  User_ID INT PRIMARY KEY,
  Password VARCHAR(10),
  User_NAME VARCHAR(50),
  User_Type VARCHAR(20) NOT NULL CHECK (User_Type IN ('Admin', 'Lecturer', 'Student'))
);


CREATE TABLE Course_Table(
  Course_id INT PRIMARY KEY,
  Course_name VARCHAR(100) NOT NULL,
  Lecturer_id INT NOT NULL,
  FOREIGN KEY (lecturer_id) REFERENCES User_table(User_ID)
);

CREATE TABLE Course_Member_Table (
  Member_ID INT PRIMARY KEY,
  Course_ID INT NOT NULL,
  Student_ID INT NOT NULL,
  FOREIGN KEY (Course_ID) REFERENCES Course_Table(Course_ID),
  FOREIGN KEY (Student_ID) REFERENCES User_table(User_ID)
);

CREATE TABLE Course_Content_Table(
  Content_ID INT PRIMARY KEY,
  Memmber_ID INT,
  Course_ID INT NOT NULL,
  Section_Name  VARCHAR(100) NOT NULL,
  Section_Content TEXT,
  FOREIGN KEY (Course_id) REFERENCES Course_table(Course_ID)
);

CREATE TABLE Discussion_Forum (
  Forum_ID INT PRIMARY KEY,
  Course_ID INT NOT NULL,
  Forum_Name VARCHAR(100) NOT NULL,
  FOREIGN KEY (course_id) REFERENCES Course_table(Course_ID)
);

CREATE TABLE Discussion_Thread_Table(
  Thread_ID INT PRIMARY KEY,
  Forum_ID INT NOT NULL, 
  Thread_Tilte VARCHAR(100) NOT NULL,
  Thread_Content TEXT,
  Parent_thread_ID INT,
  FOREIGN KEY (Forum_ID) REFERENCES Discussion_Forum_Table(Forum_ID),
  FOREIGN KEY (Parent_thread_ID) REFERENCES Discussion_Thread_Table(Thread_ID)
);

CREATE TABLE Calender_Event_Table(
  Event_ID INT PRIMARY KEY,
  Course_ID INT NOT NULL,
  Event_date DATE NOT NULL,
  Event_Description TEXT,
  FOREIGN KEY (Course_id) REFERENCES Course_Table(Course_ID)
);


CREATE TABLE Assignment (
  Assignment_id INT PRIMARY KEY,
  Course_id INT NOT NULL,
  Student_id INT NOT NULL,
  Assignment_description TEXT,
  Assignment_submission TEXT,
  Assignment_grade DECIMAL(5,2),
  FOREIGN KEY (Course_ID) REFERENCES Course_Table(Course_ID),
  FOREIGN KEY (Student_ID) REFERENCES User_Table(User_ID)
);