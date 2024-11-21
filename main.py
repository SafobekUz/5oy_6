import psycopg2

db = psycopg2.connect(
    database='magazin',
    user='postgres',
    host='localhost',
    password='1'
)
cursor = db.cursor()

#1
cursor.execute("""
    CREATE TABLE students (
        student_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER CHECK (age > 0),
        email VARCHAR(100) UNIQUE NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE courses (
        course_id SERIAL PRIMARY KEY,
        course_code VARCHAR(10) UNIQUE NOT NULL,
        course_name VARCHAR(100),
        credits INTEGER CHECK (credits BETWEEN 1 AND 5)
    );
""")

cursor.execute("""
    CREATE TABLE enrollments (
        enrollment_id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
        course_id INTEGER REFERENCES courses(course_id) ON DELETE SET NULL
    );
""")

cursor.execute("""
    CREATE TABLE teachers (
        teacher_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        experience_years INTEGER CHECK (experience_years >= 0)
    );
""")

cursor.execute("""
    CREATE TABLE course_assignments (
        assignment_id SERIAL PRIMARY KEY,
        teacher_id INTEGER REFERENCES teachers(teacher_id) ON DELETE SET DEFAULT,
        course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE
    );
""")

#2
cursor.execute("""
    INSERT INTO students (name, age, email) VALUES 
    ('Ali', 21, 'ali@example.com'),
    ('Vali', 19, 'vali@example.com'),
    ('Salim', 22, 'salim@example.com'),
    ('Nodira', 20, 'nodira@example.com'),
    ('Gulnora', 23, 'gulnora@example.com'),
    ('Umid', 24, 'umid@example.com'),
    ('Ziyoda', 18, 'ziyoda@example.com');
""")

cursor.execute("""
    INSERT INTO courses (course_code, course_name, credits) VALUES
    ('CS101', 'Python Programming', 3),
    ('CS102', 'Web Development', 4),
    ('CS103', 'Data Science', 5);
""")

cursor.execute("""
    INSERT INTO teachers (name, experience_years) VALUES
    ('Dr. Akmal', 10),
    ('Ms. Dilafruz', 5);
""")

cursor.execute("""
    INSERT INTO course_assignments (teacher_id, course_id) VALUES
    (1, 1),
    (2, 2);
""")

cursor.execute("ALTER TABLE students RENAME TO learners;")
cursor.execute("ALTER TABLE learners RENAME COLUMN name TO full_name;")

cursor.execute("UPDATE learners SET age = 25 WHERE full_name = 'Ali';")
cursor.execute("UPDATE learners SET age = 26 WHERE full_name = 'Vali';")

cursor.execute("DELETE FROM learners WHERE full_name = 'Salim';")
cursor.execute("DELETE FROM learners WHERE full_name = 'Nodira';")

db.commit()

cursor.close()
db.close()
