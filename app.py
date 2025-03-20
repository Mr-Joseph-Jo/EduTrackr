from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enables frontend to call backend

app.secret_key = 'secret_key'

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jo20042004!'
app.config['MYSQL_DB'] = 'edutrackr'

mysql = MySQL(app)





# Root route
@app.route('/')
def home():
    return render_template('index.html')

# Admin Login Route
@app.route('/api/alogin', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin_login WHERE username = %s AND password = %s', (username, password))
        record = cursor.fetchone()
        cursor.close()
        if record:
            session['loggedin'] = True
            session['username'] = record['username']
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('adminlogin.html', msg=msg)

# Define the admin dashboard route
@app.route('/admin')
def admin_dashboard():
    if 'loggedin' in session and session.get('role') == 'admin':
        return render_template('admin.html')
    return redirect(url_for('admin_login'))

# Route to check if the user is an admin and then redirect to the teacher dashboard
@app.route('/admin_to_teacher')
def admin_to_teacher():
    if 'loggedin' in session and session.get('role') == 'admin':
        return render_template('teacher.html')
    return redirect(url_for('admin_login'))






# Teacher Login Route
@app.route('/api/tlogin', methods=['GET', 'POST'])
def teacher_login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teacher_login WHERE username = %s AND password = %s', (username, password))
        record = cursor.fetchone()
        cursor.close()
        if record:
            session['loggedin'] = True
            session['username'] = record['username']
            session['role'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('teacherlogin.html', msg=msg)

# Define the teacher dashboard route
@app.route('/teacher')
def teacher_dashboard():
    if 'loggedin' in session and session.get('role') == 'teacher':
        return render_template('teacher.html')
    return redirect(url_for('teacher_login'))




# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session.get('role') == 'teacher':
            return redirect(url_for('teacher_dashboard'))
    return redirect(url_for('login_page'))





# Logout Route
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))






# Additional routes for other pages
@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/contactus')
def contact_us():
    return render_template('contactus.html')

@app.route('/loginpage')
def login_page():
    return render_template('loginpage.html')


@app.route('/api/add_teacher', methods=['POST'])
def add_teacher():
    if 'loggedin' in session and session.get('role') == 'admin':
        name = request.form['name']
        department = request.form['department']
        login = request.form['login']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO teacher (teacher_name, department) VALUES (%s, %s)', (name, department))
        teacher_id = cursor.lastrowid
        cursor.execute('INSERT INTO teacher_login (teacher_id, username, password) VALUES (%s, %s, %s)', (teacher_id, login, password))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))





# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
BATCH_FOLDER = os.path.join(UPLOAD_FOLDER, 'batches')
CLASS_FOLDER = os.path.join(UPLOAD_FOLDER, 'classes')


# Ensure the directories exist
os.makedirs(BATCH_FOLDER, exist_ok=True)
os.makedirs(CLASS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BATCH_FOLDER'] = BATCH_FOLDER
app.config['CLASS_FOLDER'] = CLASS_FOLDER



@app.route('/upload_batch', methods=['POST'])
def upload_batch():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    batch_id = request.form.get('batch')
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and batch_id:
        filename = file.filename
        file_path = os.path.join(app.config['BATCH_FOLDER'], filename)
        file.save(file_path)
        
        # Process the Excel file and update the database
        try:
            df = pd.read_excel(file_path)
            cursor = mysql.connection.cursor()
            for index, row in df.iterrows():
                print(f"Inserting row: {row.to_dict()}")  # Debugging statement
                
                # Check if batch_id exists in batches table
                cursor.execute('SELECT * FROM batches WHERE batch_id = %s', (batch_id,))
                batch = cursor.fetchone()
                
                # If batch_id does not exist, insert it into batches table
                if not batch:
                    cursor.execute('SELECT MAX(batch_id) FROM batches')
                    max_batch_id = cursor.fetchone()[0]  # Accessing the first element of the tuple
                    new_batch_id = max_batch_id + 1 if max_batch_id else 1
                    cursor.execute('INSERT INTO batches (batch_id, batch_name) VALUES (%s, %s)', 
                                   (new_batch_id, batch_id))
                    batch_id = new_batch_id
                
                # Insert data into batch_students table with batch_student_id from Excel file
                cursor.execute('INSERT INTO batch_students (batch_student_id, batch_id, student_name, uid, email) VALUES (%s, %s, %s, %s, %s)', 
                               (row['batch_student_id'], batch_id, row['student_name'], row['uid'], row['email']))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'File successfully uploaded and database updated'}), 200
        except Exception as e:
            print(f"Error processing file: {str(e)}")  # Debugging statement
            return jsonify({'message': f'Error processing file: {str(e)}'}), 500

@app.route('/upload_class', methods=['POST'])
def upload_class():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['CLASS_FOLDER'], filename)
        file.save(file_path)
        
        try:
            df = pd.read_excel(file_path)
            cursor = mysql.connection.cursor()
            for index, row in df.iterrows():
                cursor.execute('INSERT INTO students (semester_id, name, uid, subject_mark1, subject_mark2, subject_mark3, subject_mark4, subject_mark5, grade, sgpa, cgpa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                               (row['semester_id'], row['name'], row['uid'], row['subject_mark1'], row['subject_mark2'], row['subject_mark3'], row['subject_mark4'], row['subject_mark5'], row['grade'], row['sgpa'], row['cgpa']))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'File successfully uploaded and database updated'}), 200
        except Exception as e:
            return jsonify({'message': f'Error processing file: {str(e)}'}), 500



# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)