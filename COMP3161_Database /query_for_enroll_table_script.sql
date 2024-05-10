INSERT INTO OURVLE_CLONE.Enrollments (StudentID, CourseID)
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
