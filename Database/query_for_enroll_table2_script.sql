DELETE FROM OURVLE_CLONE.Enrollments WHERE StudentID IN (
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
