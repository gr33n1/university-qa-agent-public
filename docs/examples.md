## Example Queries and Outputs

### Example 1

#### Input
How many students are enrolled in each course?

#### Generated SQL
```sql
SELECT
  c.title,
  COUNT(e.student_id) AS num_students_enrolled
FROM enrollments AS e
JOIN course_offerings AS co
  ON e.offering_id = co.offering_id
JOIN courses AS c
  ON co.course_id = c.course_id
GROUP BY
  c.title;
```

#### Output

Here's the enrollment for each course:

Algorithms: 2 students
Classical Mechanics: 2 students
Databases: 5 students
Introduction to Programming: 4 students
Linear Algebra: 3 students

### Example 2
#### Input

Who teaches Databases in Fall 2025?

#### Generated SQL
```sql
SELECT t.full_name AS teacher_name
FROM course_offerings o
JOIN teachers t ON t.teacher_id = o.teacher_id
JOIN courses c ON c.course_id = o.course_id
WHERE c.title = 'Databases'
  AND o.semester = 'Fall'
  AND o.academic_year = 2025;
```
#### Output

Dr. Alice Smith teaches Databases in Fall 2025.

### Example 3
#### Input

What is the average grade in Databases in Fall 2025?

#### Generated SQL
```sql
SELECT AVG(e.grade) AS average_grade
FROM enrollments e
JOIN course_offerings o ON o.offering_id = e.offering_id
JOIN courses c ON c.course_id = o.course_id
WHERE c.title = 'Databases'
  AND o.semester = 'Fall'
  AND o.academic_year = 2025;
```
#### Output

The average grade in Databases in Fall 2025 is 88.33.

### Example 4
#### Input

Which courses is John Miller enrolled in?

#### Generated SQL
```sql
SELECT T3.title
FROM students AS T1
INNER JOIN enrollments AS T2 ON T1.student_id = T2.student_id
INNER JOIN course_offerings AS T4 ON T2.offering_id = T4.offering_id
INNER JOIN courses AS T3 ON T4.course_id = T3.course_id
WHERE T1.full_name = 'John Miller';
```

#### Output

John Miller is enrolled in:

CS101 - Introduction to Programming
CS205 - Databases
CS310 - Algorithms


### Example 5
#### Input
```sql
DELETE FROM students
```
#### Output

I couldn't complete your request: Direct SQL commands are not allowed. Please ask a natural-language question about the university database.