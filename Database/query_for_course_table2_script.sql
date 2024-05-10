-- Constraint to ensure no student can do more than 6 courses
CREATE TRIGGER MaxCoursesPerStudent
BEFORE INSERT ON Enrollments
FOR EACH ROW
BEGIN
    DECLARE num_courses INT;
    SET num_courses = (SELECT COUNT(*) FROM Enrollments WHERE StudentID = NEW.StudentID);
    IF num_courses >= 6 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A student cannot enroll in more than 6 courses';
    END IF;
END;

-- Constraint to ensure a student must be enrolled in at least 3 courses
CREATE TRIGGER MinCoursesPerStudent
BEFORE INSERT ON Enrollments
FOR EACH ROW
BEGIN
    DECLARE num_courses INT;
    SET num_courses = (SELECT COUNT(*) FROM Enrollments WHERE StudentID = NEW.StudentID);
    IF num_courses < 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A student must be enrolled in at least 3 courses';
    END IF;
END;

-- Constraint to ensure each course must have at least 10 members
CREATE TRIGGER MinMembersPerCourse
BEFORE INSERT ON Enrollments
FOR EACH ROW
BEGIN
    DECLARE num_members INT;
    SET num_members = (SELECT COUNT(*) FROM Enrollments WHERE CourseID = NEW.CourseID);
    IF num_members >= 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Each course must have at least 10 members';
    END IF;
END;

-- Constraint to ensure no lecturer can teach more than 5 courses
CREATE TRIGGER MaxCoursesPerLecturer
BEFORE INSERT ON Courses
FOR EACH ROW
BEGIN
    DECLARE num_courses INT;
    SET num_courses = (SELECT COUNT(*) FROM Courses WHERE LecturerID = NEW.LecturerID);
    IF num_courses >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No lecturer can teach more than 5 courses';
    END IF;
END;

-- Constraint to ensure a lecturer must teach at least 1 course
CREATE TRIGGER MinCoursesPerLecturer
BEFORE INSERT ON Courses
FOR EACH ROW
BEGIN
    DECLARE num_courses INT;
    SET num_courses = (SELECT COUNT(*) FROM Courses WHERE LecturerID = NEW.LecturerID);
    IF num_courses = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A lecturer must teach at least 1 course';
    END IF;
END;
