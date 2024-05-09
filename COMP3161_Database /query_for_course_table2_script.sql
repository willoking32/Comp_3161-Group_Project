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