-- View to select all students
CREATE VIEW AllStudents AS
SELECT *
FROM Users
WHERE UserType = 'student';

-- View to select all courses
CREATE VIEW AllCourses AS
SELECT *
FROM Courses;

-- View to select students with their enrolled courses count
CREATE VIEW StudentCourseCount AS
SELECT StudentID, COUNT(*) AS EnrolledCoursesCount
FROM Enrollments
GROUP BY StudentID;

-- View to select students with less than 6 courses
CREATE VIEW StudentsWithLessThanSixCourses AS
SELECT StudentID
FROM StudentCourseCount
WHERE EnrolledCoursesCount < 6;

-- View to select students with at least 3 courses
CREATE VIEW StudentsWithAtLeastThreeCourses AS
SELECT StudentID
FROM StudentCourseCount
WHERE EnrolledCoursesCount >= 3;

-- View to select courses with at least 10 members
CREATE VIEW CoursesWithAtLeastTenMembers AS
SELECT CourseID, COUNT(*) AS MembersCount
FROM Enrollments
GROUP BY CourseID
HAVING MembersCount >= 10;

-- View to select lecturers with their taught courses count
CREATE VIEW LecturerCourseCount AS
SELECT LecturerID, COUNT(*) AS TaughtCoursesCount
FROM Courses
GROUP BY LecturerID;

-- View to select lecturers with less than 5 courses
CREATE VIEW LecturersWithLessThanFiveCourses AS
SELECT LecturerID
FROM LecturerCourseCount
WHERE TaughtCoursesCount < 5;

-- View to select lecturers with at least 1 course
CREATE VIEW LecturersWithAtLeastOneCourse AS
SELECT LecturerID
FROM LecturerCourseCount
WHERE TaughtCoursesCount >= 1;