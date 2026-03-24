PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS course_offerings;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;

CREATE TABLE teachers (
    teacher_id     INTEGER PRIMARY KEY,
    full_name      TEXT NOT NULL,
    email          TEXT UNIQUE,
    department     TEXT
);

CREATE TABLE students (
    student_id     INTEGER PRIMARY KEY,
    full_name      TEXT NOT NULL,
    email          TEXT UNIQUE,
    major          TEXT,
    year_of_study  INTEGER CHECK (year_of_study BETWEEN 1 AND 8)
);

CREATE TABLE courses (
    course_id      INTEGER PRIMARY KEY,
    course_code    TEXT NOT NULL UNIQUE,
    title          TEXT NOT NULL,
    credits        INTEGER NOT NULL CHECK (credits > 0),
    department     TEXT
);

CREATE TABLE course_offerings (
    offering_id    INTEGER PRIMARY KEY,
    course_id      INTEGER NOT NULL,
    teacher_id     INTEGER NOT NULL,
    semester       TEXT NOT NULL CHECK (semester IN ('Fall', 'Spring', 'Summer')),
    academic_year  INTEGER NOT NULL CHECK (academic_year >= 2000),
    section_number TEXT NOT NULL DEFAULT '001',
    capacity       INTEGER NOT NULL CHECK (capacity > 0),

    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,

    UNIQUE (course_id, teacher_id, semester, academic_year, section_number)
);

CREATE TABLE enrollments (
    enrollment_id  INTEGER PRIMARY KEY,
    student_id     INTEGER NOT NULL,
    offering_id    INTEGER NOT NULL,
    grade          REAL CHECK (grade BETWEEN 0 AND 100),
    enrolled_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE,

    UNIQUE (student_id, offering_id)
);

CREATE INDEX idx_students_name
    ON students(full_name);

CREATE INDEX idx_teachers_name
    ON teachers(full_name);

CREATE INDEX idx_courses_code
    ON courses(course_code);

CREATE INDEX idx_courses_title
    ON courses(title);

CREATE INDEX idx_offerings_lookup
    ON course_offerings(course_id, teacher_id, semester, academic_year);

CREATE INDEX idx_enrollments_student
    ON enrollments(student_id);

CREATE INDEX idx_enrollments_offering
    ON enrollments(offering_id);