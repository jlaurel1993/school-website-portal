-- 1. Create the database shell
CREATE DATABASE IF NOT EXISTS classroom_db;

-- 2. Switch to using this database
USE classroom_db;

-- 3. Create the permanent students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT,
    grade_level VARCHAR(20),
    math VARCHAR(5),
    reading VARCHAR(5),
    notes TEXT,
    math_hw_url Text,
    reading_hw_url Text,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Clear out any old rows and add the 3 starting students
TRUNCATE TABLE students;
INSERT INTO students (first_name, last_name, age, grade_level, math, reading, notes) VALUES
('Tia', 'Laurel', 26, '3rd Grade', 'A+', 'A', 'Super helper during clean up.'),
('Grandma', 'Laurel', 56, '3rd Grade', 'B', 'A+', 'Great listener, loves reading aloud.'),
('Noah', 'Gonzalez', 5, '4th Grade', 'A', 'B-', 'Wiggles a lot, but works hard.');
