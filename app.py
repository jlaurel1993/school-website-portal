from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Dynamic Database Connection Routing
def get_db_connection():
    db_host = os.environ.get("DB_HOST", "localhost")
    return mysql.connector.connect(
        host=db_host,
        user="root",
        password="Gradebook2026!",
        database="classroom_db"
    )

# --- AUTOMATIC ROSTER SEED ENGINE ---
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

# Helper function to turn database list into a dictionary for your HTML
def transform_to_html_dict(student_list):
    # Converts rows into { id: { first_name: ..., last_name: ... } }
    # This ensures '{% for id, details in all_students.items() %}' works flawlessly!
    student_dict = {}
    for student in student_list:
        student_dict[student['id']] = student
    return student_dict

# --- 1. MAIN LIVE ROSTER VIEW ---
@app.route('/')
def index():
    try:
        seed_database_if_empty()
    except Exception as e:
        print(f"Database seeding skipped: {e}")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM students ORDER BY last_name ASC")
    raw_students = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Format the data to match your template requirements
    students_formatted = transform_to_html_dict(raw_students)
    return render_template('index.html', all_students=students_formatted, search_result=None, search_query=None)

# --- 2. MATCHED ENROLLMENT INTAKE ---
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
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

# --- 3. MATCHED SEARCH ENGINE ---
@app.route('/search', methods=['GET'])
def search_student():
    student_id = request.args.get('student_id', '').strip()
    search_query = request.args.get('query', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM students ORDER BY last_name ASC")
    raw_students = cursor.fetchall()
    
    search_result = None
    if student_id:
        query = "SELECT * FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))
        search_result = cursor.fetchall()
    elif search_query:
        query = "SELECT * FROM students WHERE first_name LIKE %s OR last_name LIKE %s"
        cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
        search_result = cursor.fetchall()
        
    cursor.close()
    conn.close()
    
    students_formatted = transform_to_html_dict(raw_students)
    return render_template('index.html', all_students=students_formatted, search_result=search_result, search_query=search_query or student_id)

# --- 4. RECORD REMOVAL MACRO ---
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
    
