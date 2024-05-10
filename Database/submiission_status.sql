
ALTER TABLE OURVLE_CLONE.Assignments
ADD SubmitStatus ENUM('submitted', 'pending', 'late', 'not submitted') DEFAULT 'pending';


UPDATE OURVLE_CLONE.Assignments
SET SubmitStatus = 'pending';
