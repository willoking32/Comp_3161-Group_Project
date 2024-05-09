-- Users table
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    Password VARCHAR(50),
    UserType ENUM('admin', 'lecturer', 'student')
);

-- Courses table
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100),
    LecturerID INT,
    FOREIGN KEY (LecturerID) REFERENCES Users(UserID)
);

-- Enrollments table
CREATE TABLE Enrollments (
    EnrollmentID INT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    FOREIGN KEY (StudentID) REFERENCES Users(UserID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Calendar Events table
CREATE TABLE CalendarEvents (
    EventID INT PRIMARY KEY,
    CourseID INT,
    EventDate DATE,
    EventDescription TEXT,
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Forums table
CREATE TABLE Forums (
    ForumID INT PRIMARY KEY,
    CourseID INT,
    ForumName VARCHAR(100),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Discussion Threads table
CREATE TABLE DiscussionThreads (
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
CREATE TABLE CourseContent (
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
CREATE TABLE Assignments (
    AssignmentID INT PRIMARY KEY,
    CourseID INT,
    StudentID INT,
    AssignmentName VARCHAR(100),
    Grade DECIMAL(5, 2),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    FOREIGN KEY (StudentID) REFERENCES Users(UserID)
);

-- Create the view CoursesWith50OrMoreStudents
CREATE VIEW CoursesWith50OrMoreStudents AS
SELECT Courses.*
FROM Courses
WHERE CourseID IN (
    SELECT CourseID
    FROM Enrollments
    GROUP BY CourseID
    HAVING COUNT(StudentID) >= 50
);

-- Verify the subquery results
SELECT CourseID
FROM Enrollments
GROUP BY CourseID
HAVING COUNT(StudentID) >= 50;

-- Insert statements for initial data population
INSERT INTO Users (UserID, Username, Password, UserType)
SELECT 
    (t.num - 1) AS UserID,
    CONCAT('student', t.num - 1) AS Username,
    'student_password' AS Password,
    'student' AS UserType
FROM 
    (SELECT @num := @num + 1 AS num
     FROM (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) t1,
          (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) t2,
          (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) t3,
          (SELECT @num := 0) n) t
WHERE t.num <= 100000;

-- Insert 200 courses
INSERT INTO Courses (CourseID, CourseName, LecturerID)
SELECT 
    (ROW_NUMBER() OVER () - 1) AS CourseID,
    CONCAT('Course', ROW_NUMBER() OVER () - 1) AS CourseName,
    ((ROW_NUMBER() OVER () - 1) % 100) + 1 AS LecturerID -- Assign lecturers in a cyclical manner
FROM 
    generate_series(1, 200);



-- Ensure no lecturer teaches more than 5 courses and each lecturer teaches at least 1 course
DELETE FROM OURVLE_CLONE.Courses WHERE CourseID IN (
    SELECT CourseID
    FROM (
        SELECT 
            LecturerID,
            COUNT(*) AS CourseCount
        FROM 
            Courses
        GROUP BY 
            LecturerID
    ) AS LecturerCourseCount
    WHERE 
        CourseCount > 5
);

-- Ensure each student is enrolled in at least 3 courses and no more than 6 courses
DELETE FROM Enrollments WHERE StudentID IN (
    SELECT StudentID
    FROM (
        SELECT 
            StudentID,
            COUNT(*) AS CourseCount
        FROM 
            Enrollments
        GROUP BY 
            StudentID
    ) AS StudentCourseCount
    WHERE 
        CourseCount < 3 OR CourseCount > 6
);


-- Ensure each course has at least 10 members
INSERT INTO Enrollments (StudentID, CourseID)
SELECT 
    StudentID,
    CourseID
FROM 
    (
        SELECT 
            StudentID,
            CourseID,
            ROW_NUMBER() OVER (PARTITION BY CourseID ORDER BY RAND()) AS RowNum
        FROM 
            Enrollments
    ) AS Subquery
WHERE 
    RowNum <= 10;



-- CRUD operations for Users, Courses, Enrollments, CalendarEvents, Forums, DiscussionThreads, CourseContent, Assignments
