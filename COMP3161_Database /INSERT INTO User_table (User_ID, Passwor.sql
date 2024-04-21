INSERT INTO User_table (User_ID, Password, User_NAME, User_Type)
VALUES
  (1, 'password1', 'admin1', 'Admin'),
  (2, 'password2', 'lecturer1', 'Lecturer'),
  (3, 'password3', 'student1', 'Student');

INSERT INTO Course_Table (Course_id, Course_name, Lecturer_id)
VALUES
  (1, 'Course 1', 2),
  (2, 'Course 2', 2),
  (3, 'Course 3', 2);

INSERT INTO Course_Member_Table (Member_ID, Course_ID, Student_ID)
VALUES
  (1, 1, 3),
  (2, 2, 3),
  (3, 3, 3);

INSERT INTO Course_Content_Table (Content_ID, Memmber_ID, Course_ID, Section_Name, Section_Content)
VALUES
  (1, NULL, 1, 'Section 1', 'Content for Section 1'),
  (2, NULL, 1, 'Section 2', 'Content for Section 2'),
  (3, NULL, 2, 'Section 1', 'Content for Section 1');

INSERT INTO Discussion_Forum (Forum_ID, Course_ID, Forum_Name)
VALUES
  (1, 1, 'Forum 1'),
  (2, 2, 'Forum 2');

INSERT INTO Discussion_Thread_Table (Thread_ID, Forum_ID, Thread_Tilte, Thread_Content, Parent_thread_ID)
VALUES
  (1, 1, 'Thread 1', 'Thread content 1', NULL),
  (2, 1, 'Thread 2', 'Thread content 2', NULL),
  (3, 2, 'Thread 1', 'Thread content 1', NULL);

INSERT INTO Calender_Event_Table (Event_ID, Course_ID, Event_date, Event_Description)
VALUES
  (1, 1, '2024-04-19', 'Event for Course 1'),
  (2, 2, '2024-04-20', 'Event for Course 2');

INSERT INTO Assignment (Assignment_id, Course_id, Student_id, Assignment_description, Assignment_submission, Assignment_grade)
VALUES
  (1, 1, 3, 'Assignment 1 for Course 1', 'Submission for Assignment 1', 90.5),
  (2, 1, 3, 'Assignment 2 for Course 1', 'Submission for Assignment 2', 85.0);
