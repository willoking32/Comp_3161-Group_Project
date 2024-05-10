CREATE DATABASE OURVLE_CLONE;

    -- Users table
CREATE TABLE OURVLE_CLONE.Users (
    UserID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Password VARCHAR(50),
    UserType ENUM('admin', 'lecturer', 'student')
);

-- Courses table
CREATE TABLE OURVLE_CLONE.Courses (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100),
    LecturerID INT,
    FOREIGN KEY (LecturerID) REFERENCES Users(UserID)
);

-- Enrollments table
CREATE TABLE OURVLE_CLONE.Enrollments (
    EnrollmentID INT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    FOREIGN KEY (StudentID) REFERENCES Users(UserID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Calendar Events table
CREATE TABLE OURVLE_CLONE.CalendarEvents (
    EventID INT PRIMARY KEY,
    CourseID INT,
    EventDate DATE,
    EventDescription TEXT,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Forums table
CREATE TABLE OURVLE_CLONE.Forums (
    ForumID INT PRIMARY KEY,
    CourseID INT,
    ForumName VARCHAR(100),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Discussion Threads table
CREATE TABLE OURVLE_CLONE.DiscussionThreads (
    ThreadID INT PRIMARY KEY,
    ForumID INT,
    UserID INT,
    ThreadTitle VARCHAR(100),
    ThreadPost TEXT,
    ParentThreadID INT, -- for replies
    FOREIGN KEY (ForumID) REFERENCES Forums(ForumID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ParentThreadID) REFERENCES DiscussionThreads(ThreadID)
);

-- Course Content table
CREATE TABLE OURVLE_CLONE.CourseContent (
    ContentID INT PRIMARY KEY,
    CourseID INT,
    LecturerID INT,
    ContentType ENUM('link', 'file', 'slides'),
    ContentDescription TEXT,
    SectionName VARCHAR(100),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (LecturerID) REFERENCES Users(UserID)
);

-- Assignments table
CREATE TABLE OURVLE_CLONE.Assignments (
    AssignmentID INT PRIMARY KEY,
    CourseID INT,
    StudentID INT,
    AssignmentName VARCHAR(100),
    Grade DECIMAL(5, 2),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (StudentID) REFERENCES Users(UserID)
);









-- CREATE VIEW CoursesWith50PlusStudents AS
-- SELECT c.CourseID, c.CourseName, COUNT(e.StudentID) AS StudentCount
-- FROM Courses c
-- JOIN Enrollments e ON c.CourseID = e.CourseID
-- GROUP BY c.CourseID, c.CourseName
-- HAVING COUNT(e.StudentID) >= 50;



-- CREATE VIEW StudentsIn5PlusCourses AS
-- SELECT e.StudentID, COUNT(e.CourseID) AS CourseCount
-- FROM Enrollments e
-- GROUP BY e.StudentID
-- HAVING COUNT(e.CourseID) >= 5;


-- CREATE VIEW LecturersTeaching3PlusCourses AS
-- SELECT u.UserID, u.FirstName, u.LastName, COUNT(c.CourseID) AS CourseCount
-- FROM Users u
-- JOIN Courses c ON u.UserID = c.LecturerID
-- GROUP BY u.UserID, u.FirstName, u.LastName
-- HAVING COUNT(c.CourseID) >= 3;


-- CREATE VIEW Top10EnrolledCourses AS
-- SELECT c.CourseID, c.CourseName, COUNT(e.StudentID) AS EnrollmentCount
-- FROM Courses c
-- JOIN Enrollments e ON c.CourseID = e.CourseID
-- GROUP BY c.CourseID, c.CourseName
-- ORDER BY COUNT(e.StudentID) DESC
-- LIMIT 10;

-- CREATE VIEW Top10StudentsWithHighestAverages AS
-- SELECT g.StudentID, AVG(g.Grade) AS AverageGrade
-- FROM Assignment g
-- GROUP BY g.StudentID
-- ORDER BY AVG(g.Grade) DESC
-- LIMIT 10;
