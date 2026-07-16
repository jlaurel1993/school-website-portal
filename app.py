from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='.')

# This helper function opens a secure connection straight to our MySQL filing cabinet
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gradebook2026!",
        database="classroom_db"
    )

# ─── 1. THE HOME PAGE ROUTE ───
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) # dictionary=True makes results clean to read
    
    # Grab the full roster of students from our permanent table
    cursor.execute("SELECT id, first_name, last_name, grade_level FROM students")
    students_list = cursor.fetchall()
    
    # Format the data so it feeds seamlessly into our existing HTML table loop
    all_students = {row['id']: row for row in students_list}
    
    cursor.close()
    conn.close()
    return render_template('index.html', student=None, error=None, all_students=all_students)

# ─── 2. THE SEARCH ROUTE ───
@app.route('/search', methods=['GET'])
def search_student():
    search_id = request.args.get('student_id')
    
    # We must always fetch the roster so the attendance sheet stays visible during a search
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, last_name, grade_level FROM students")
    all_students = {row['id']: row for row in cursor.fetchall()}
    
    if search_id:
        try:
            search_id = int(search_id)
            # Safely query the database for the matching student ID row
            cursor.execute("SELECT * FROM students WHERE id = %s", (search_id,))
            found_student = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if found_student:
                return render_template('index.html', student=found_student, error=None, all_students=all_students)
            else:
                return render_template('index.html', student=None, error="Student ID not found!", all_students=all_students)
        except ValueError:
            cursor.close()
            conn.close()
            return render_template('index.html', student=None, error="Please enter a valid number.", all_students=all_students)
            
    cursor.close()
    conn.close()
    return render_template('index.html', student=None, error=None, all_students=all_students)

# ─── 3. THE ADD STUDENT ROUTE ───
@app.route('/add_student', methods=['POST'])
def add_student():
    # Capture everything your daughter types into the enrollment form boxes
    first = request.form.get('first_name')
    last = request.form.get('last_name')
    age = request.form.get('age')
    grade_lvl = request.form.get('grade_level')
    math = request.form.get('math_grade') or 'A'
    reading = request.form.get('reading_grade') or 'A'
    notes = request.form.get('notes') or 'No notes yet.'

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert a brand new row! MySQL automatically handles calculating next_id for us.
    query = """
        INSERT INTO students (first_name, last_name, age, grade_level, math, reading, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (first, last, age, grade_lvl, math, reading, notes))
    
    conn.commit() # Critical: This officially saves the new student row onto the hard drive!
    cursor.close()
    conn.close()
    
    return redirect(url_for('home'))

# ─── 4. THE DELETE STUDENT ROUTE ───
@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute the SQL delete query targeting the specific ID
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    
    conn.commit() # Lock the changes into the hard drive!
    cursor.close()
    conn.close()
    
    # Send her right back to the home page, where the student will be missing from the table!
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
