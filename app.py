from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Dynamic Database Connection Routing
def get_db_connection():
    # Looks for Render's internal network environment variable; 
    # Defaults back to 'localhost' if you run it at home on your PC
    db_host = os.environ.get("DB_HOST", "localhost")
    
    return mysql.connector.connect(
        host=db_host,
        user="root",
        password="Gradebook2026!",
        database="classroom_db"
    )

# --- 1. MAIN LIVE ROSTER VIEW ---
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all students sorted alphabetically by last name
    cursor.execute("SELECT * FROM students ORDER BY last_name ASC")
    students = cursor.fetchall()
    
    cursor.close()
    conn.close()
    # Passed as all_students to sync perfectly with your template's Jinja loop
    return render_template('index.html', all_students=students, search_result=None, search_query=None)

# --- 2. DIGITAL ENROLLMENT INTAKE (ADD) ---
@app.route('/add', methods=['POST'])
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

# --- 3. DYNAMIC SEARCH ENGINE (LOOKUP) ---
@app.route('/search', methods=['GET'])
def search_student():
    search_query = request.args.get('query', '').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch full roster to keep the main layout filled
    cursor.execute("SELECT * FROM students ORDER BY last_name ASC")
    students = cursor.fetchall()
    
    # Run exact or partial matching against first name or last name
    search_result = None
    if search_query:
        query = "SELECT * FROM students WHERE first_name LIKE %s OR last_name LIKE %s"
        cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
        search_result = cursor.fetchall()
        
    cursor.close()
    conn.close()
    
    # Passed as all_students here as well to protect template rendering stability
    return render_template('index.html', all_students=students, search_result=search_result, search_query=search_query)

# --- 4. RECORD REMOVAL MACRO (DELETE) ---
@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Target and purge the row matching the specific unique primary ID index
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
