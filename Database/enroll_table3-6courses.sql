INSERT INTO OURVLE_CLONE.Enrollments (StudentID, CourseID)
SELECT 
    U.UserID AS StudentID,
    MIN(C.CourseID) AS CourseID
FROM 
    OURVLE_CLONE.Users AS U
JOIN 
    OURVLE_CLONE.Courses AS C
    ON C.LecturerID <> U.UserID
WHERE 
    U.UserType = 'student'
GROUP BY 
    U.UserID
HAVING 
    COUNT(*) BETWEEN 3 AND 6;
