INSERT INTO teachers (teacher_id, full_name, email, department) VALUES
(1, 'Dr. Alice Smith', 'alice.smith@univ.edu', 'Computer Science'),
(2, 'Dr. Bob Johnson', 'bob.johnson@univ.edu', 'Mathematics'),
(3, 'Dr. Carol Lee', 'carol.lee@univ.edu', 'Computer Science'),
(4, 'Dr. David Cohen', 'david.cohen@univ.edu', 'Physics');

INSERT INTO students (student_id, full_name, email, major, year_of_study) VALUES
(1, 'John Miller', 'john.miller@univ.edu', 'Computer Science', 2),
(2, 'Emma Davis', 'emma.davis@univ.edu', 'Mathematics', 1),
(3, 'Noah Wilson', 'noah.wilson@univ.edu', 'Computer Science', 3),
(4, 'Olivia Brown', 'olivia.brown@univ.edu', 'Physics', 2),
(5, 'Liam Taylor', 'liam.taylor@univ.edu', 'Computer Science', 4),
(6, 'Sophia Green', 'sophia.green@univ.edu', 'Mathematics', 2);

INSERT INTO courses (course_id, course_code, title, credits, department) VALUES
(1, 'CS101', 'Introduction to Programming', 4, 'Computer Science'),
(2, 'CS205', 'Databases', 3, 'Computer Science'),
(3, 'CS310', 'Algorithms', 4, 'Computer Science'),
(4, 'MATH201', 'Linear Algebra', 3, 'Mathematics'),
(5, 'PHYS210', 'Classical Mechanics', 4, 'Physics');

INSERT INTO course_offerings (offering_id, course_id, teacher_id, semester, academic_year, section_number, capacity) VALUES
(1, 1, 1, 'Fall',   2025, '001', 50),
(2, 2, 1, 'Fall',   2025, '001', 40),
(3, 3, 3, 'Spring', 2026, '001', 35),
(4, 4, 2, 'Fall',   2025, '001', 60),
(5, 2, 3, 'Spring', 2026, '001', 45),
(6, 5, 4, 'Fall',   2025, '001', 30);

INSERT INTO enrollments (enrollment_id, student_id, offering_id, grade) VALUES
(1, 1, 1, 88),
(2, 2, 1, 91),
(3, 3, 1, 79),
(4, 6, 1, 84),

(5, 1, 2, 85),
(6, 3, 2, 93),
(7, 5, 2, 87),

(8, 2, 4, 95),
(9, 4, 4, 82),
(10, 6, 4, 89),

(11, 1, 3, 90),
(12, 5, 3, 84),

(13, 3, 5, 89),
(14, 4, 5, 76),

(15, 4, 6, 88),
(16, 2, 6, 81);