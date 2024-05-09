INSERT INTO OURVLE_CLONE.Users (UserID, Username, Password, UserType)
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