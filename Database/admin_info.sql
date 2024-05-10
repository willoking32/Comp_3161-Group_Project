INSERT INTO Users (UserID, Username, Password, UserType)
SELECT 
    (ROW_NUMBER() OVER () - 1) AS UserID,
    CONCAT('admin', ROW_NUMBER() OVER () - 1) AS Username,
    CONCAT('admin_password', ROW_NUMBER() OVER () - 1) AS Password,
    'admin' AS UserType
FROM 
    (SELECT 0 AS dummy UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) t1,
    (SELECT 0 AS dummy UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) t2
LIMIT 10;