from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

def get_db_connection():
    db_host = os.environ.get("DB_HOST", "localhost")
    return mysql.connector.connect(
        host=db_host,
        user="root",
        password="Gradebook2026!",
        database="classroom_db"
    )

def seed_database_if_empty():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    if count == 0:
        default_students = [
            ("Alex", "Baker", 10, "5th Grade", "A", "B+", "Enjoys reading historical fiction."),
            ("Chloe", "Davis", 11, "5th Grade", "A-", "A", "Excellent participation in science labs."),
            ("Marcus", "Evans", 10, "5th Grade", "B", "A-", "Requires extra time on math tests.")
        ]
        query = """
            INSERT INTO students (first_name, last_name, age, grade_level, math, reading, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(query, default_students)
        conn.commit()
    cursor.close()
    conn.close()

def attach_homework_to_students(students, cursor):
    """Helper function to fetch all homework files for a list of students."""
    if not students:
        return students
    
    student_ids = [s['id'] for s in students]
    format_strings = ','.join(['%s'] * len(student_ids))
    
    hw_query = f"SELECT * FROM homework WHERE student_id IN ({format_strings}) ORDER BY uploaded_at DESC"
    cursor.execute(hw_query, tuple(student_ids))
    hw_records = cursor.fetchall()
    
    # Map homework records to student IDs
    hw_by_student = {}
    for record in hw_records:
        sid = record['student_id']
        if sid not in hw_by_student:
            hw_by_student[sid] = {'math': [], 'reading': []}
        
        subj = record['subject'].lower()
        if subj in hw_by_student[sid]:
            hw_by_student[sid][subj].append(record)
            
    for student in students:
        student['math_hw_list'] = hw_by_student.get(student['id'], {}).get('math', [])
        student['reading_hw_list'] = hw_by_student.get(student['id'], {}).get('reading', [])
        
    return students

@app.route('/')
def index():
    try:
        seed_database_if_empty()
    except Exception as e:
        print(f"Database seeding skipped: {e}")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students ORDER BY last_name ASC")
    students = cursor.fetchall()
    
    students = attach_homework_to_students(students, cursor)
    
    cursor.close()
    conn.close()
    return render_template('index.html', all_students=students, search_result=None, search_query=None)

@app.route('/add_student', methods=['POST'])
def add_student():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age')
    grade_level = request.form.get('grade_level')
    math = request.form.get('math')
    reading = request.form.get('reading')
    notes = request.form.get('notes')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO students (first_name, last_name, age, grade_level, math, reading, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (first_name, last_name, age, grade_level, math, reading, notes))
    student_id = cursor.lastrowid

    # Handle optional Math HW upload on enrollment
    math_hw_file = request.files.get('math_hw')
    if math_hw_file and math_hw_file.filename != '':
        upload_result = cloudinary.uploader.upload(math_hw_file)
        file_url = upload_result.get('secure_url')
        cursor.execute("INSERT INTO homework (student_id, subject, file_url) VALUES (%s, %s, %s)",
                       (student_id, 'math', file_url))

    # Handle optional Reading HW upload on enrollment
    reading_hw_file = request.files.get('reading_hw')
    if reading_hw_file and reading_hw_file.filename != '':
        upload_result = cloudinary.uploader.upload(reading_hw_file)
        file_url = upload_result.get('secure_url')
        cursor.execute("INSERT INTO homework (student_id, subject, file_url) VALUES (%s, %s, %s)",
                       (student_id, 'reading', file_url))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/upload_hw/<int:student_id>', methods=['POST'])
def upload_hw(student_id):
    subject = request.form.get('subject')  # 'math' or 'reading'
    hw_file = request.files.get('hw_file')

    if hw_file and hw_file.filename != '':
        upload_result = cloudinary.uploader.upload(hw_file)
        file_url = upload_result.get('secure_url')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO homework (student_id, subject, file_url) VALUES (%s, %s, %s)",
                       (student_id, subject, file_url))
        conn.commit()
        cursor.close()
        conn.close()

    search_query = request.args.get('query', '')
    if search_query:
        return redirect(url_for('search_student', query=search_query))
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_student():
    search_query = request.args.get('query', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students ORDER BY last_name ASC")
    students = cursor.fetchall()
    students = attach_homework_to_students(students, cursor)
    
    search_result = None
    if search_query:
        query = "SELECT * FROM students WHERE first_name LIKE %s OR last_name LIKE %s"
        cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
        search_result = cursor.fetchall()
        search_result = attach_homework_to_students(search_result, cursor)
        
    cursor.close()
    conn.close()
    return render_template('index.html', all_students=students, search_result=search_result, search_query=search_query)

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
