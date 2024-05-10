
-- Maximum courses per student
SELECT MAX(EnrolledCoursesCount) AS MaxCoursesPerStudent
FROM (
    SELECT COUNT(*) AS EnrolledCoursesCount
    FROM Enrollments
    GROUP BY StudentID
) AS StudentCourseCount;

-- Minimum courses per student
SELECT MIN(EnrolledCoursesCount) AS MinCoursesPerStudent
FROM (
    SELECT COUNT(*) AS EnrolledCoursesCount
    FROM Enrollments
    GROUP BY StudentID
) AS StudentCourseCount;

-- Course with the least members
SELECT CourseID, COUNT(*) AS MembersCount
FROM Enrollments
GROUP BY CourseID
ORDER BY MembersCount ASC
LIMIT 1;

-- Lecturer with maximum courses
SELECT LecturerID, COUNT(*) AS TaughtCoursesCount
FROM Courses
GROUP BY LecturerID
ORDER BY TaughtCoursesCount DESC
LIMIT 1;

-- Lecturer with minimum courses
SELECT LecturerID, COUNT(*) AS TaughtCoursesCount
FROM Courses
GROUP BY LecturerID
ORDER BY TaughtCoursesCount ASC
LIMIT 1;

SELECT CourseID, COUNT(*) AS MembersCount
FROM Enrollments
GROUP BY CourseID
ORDER BY MembersCount DESC
LIMIT 1;
