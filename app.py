from flask import Flask, request, jsonify, session, render_template, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
from dotenv import load_dotenv
from flask_cors import CORS
import os
import pandas as pd

load_dotenv()


app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enables frontend to call backend

app.secret_key = 'secret_key'

# Database Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'edutrackr')

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
        cursor.execute('SELECT * FROM adminlogin WHERE username = %s AND password = %s', (username, password))
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
        cursor.execute('INSERT INTO teacher (teacher_name, department, login_id, password) VALUES (%s, %s, %s, %s)',
                       (name, department, login, password))

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
                cursor.execute('INSERT INTO batch_students (batch_id, student_name, uid, email) VALUES (%s, %s, %s, %s)', 
                               (row['batch_id'], row['student_name'], row['uid'], row['email']))
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

            # Normalize column names (strip spaces and make lowercase)
            df.columns = df.columns.str.strip().str.lower()

            # Ensure required columns exist
            required_columns = {'uid', 'batch', 'semester_id', 'semester_name', 'name'}
            if not required_columns.issubset(df.columns):
                return jsonify({'message': 'Missing required columns in the file'}), 400

            cursor = mysql.connection.cursor()

            for index, row in df.iterrows():
                semester_id = row['semester_id']

                # Validate semester_id
                if pd.isna(semester_id) or not isinstance(semester_id, (int, float)):
                    return jsonify({'message': f'Invalid Semester ID at row {index + 2}'}), 400

                cursor.execute('SELECT * FROM sem WHERE semester_id = %s', (int(semester_id),))
                semester = cursor.fetchone()
                if not semester:
                    return jsonify({'message': f'Semester ID {int(semester_id)} does not exist'}), 400

                # Determine target table
                table_name = 's1' if int(semester_id) == 1 else 's2' if int(semester_id) == 2 else None
                if not table_name:
                    return jsonify({'message': f'Invalid semester ID {int(semester_id)}'}), 400

                # Define column mappings for each table
                if table_name == 's1':
                    query = f'''
                        INSERT INTO {table_name} (
                            UID, Batch, Semester_id, Semester_name, Name, 
                            LAC_Marks, LAC_Grade, Engg_Chem_Marks, Engg_Chem_Grade, Engg_Graphics_Marks, Engg_Graphics_Grade, 
                            Basics_CE_ME_Marks, Basics_CE_ME_Grade, LS_Marks, LS_Grade, Chem_Lab_Marks, Chem_Lab_Grade, 
                            Workshop_Marks, Workshop_Grade, sgpa, cgpa
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    values = (
                        row.get('uid'), row.get('batch'), int(semester_id), row.get('semester_name'), row.get('name'),
                        row.get('lac_marks', 0), row.get('lac_grade', ''),
                        row.get('engg_chem_marks', 0), row.get('engg_chem_grade', ''),
                        row.get('engg_graphics_marks', 0), row.get('engg_graphics_grade', ''),
                        row.get('basics_ce_me_marks', 0), row.get('basics_ce_me_grade', ''),
                        row.get('ls_marks', 0), row.get('ls_grade', ''),
                        row.get('chem_lab_marks', 0), row.get('chem_lab_grade', ''),
                        row.get('workshop_marks', 0), row.get('workshop_grade', ''),
                        row.get('sgpa', 0), row.get('cgpa', 0)
                    )
                elif table_name == 's2':
                    query = f'''
                        INSERT INTO {table_name} (
                            UID, Batch, Semester_id, Semester_name, Name,
                            Vector_calculus_Marks, Vector_calculus_grade, Engg_Physics_Marks, Engg_Physics_grade, 
                            Engg_Mechanics_Marks, Engg_Mechanics_grade, Professional_Communication_Marks, Professional_Communication_Grade, 
                            Basics_of_Electronic_and_Electricals_Marks, Basics_of_Electronic_and_Electricals_grade,
                            Programming_in_C_Marks, Programming_in_C_grade, engg_physics_lab_Marks, engg_physics_lab_grade, 
                            Electrical_electronic_lab_mark, Electrical_electronic_lab_grade, sgpa, cgpa
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    values = (
                        row.get('uid'), row.get('batch'), int(semester_id), row.get('semester_name'), row.get('name'),
                        row.get('vector_calculus_marks', 0), row.get('vector_calculus_grade', ''),
                        row.get('engg_physics_marks', 0), row.get('engg_physics_grade', ''),
                        row.get('engg_mechanics_marks', 0), row.get('engg_mechanics_grade', ''),
                        row.get('professional_communication_marks', 0), row.get('professional_communication_grade', ''),
                        row.get('basics_of_electronic_and_electricals_marks', 0), row.get('basics_of_electronic_and_electricals_grade', ''),
                        row.get('programming_in_c_marks', 0), row.get('programming_in_c_grade', ''),
                        row.get('engg_physics_lab_marks', 0), row.get('engg_physics_lab_grade', ''),
                        row.get('electrical_electronic_lab_mark', 0), row.get('electrical_electronic_lab_grade', ''),
                        row.get('sgpa', 0), row.get('cgpa', 0)
                    )

                cursor.execute(query, values)

            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': f'File successfully uploaded to {table_name} and database updated'}), 200

        except Exception as e:
            return jsonify({'message': f'Error processing file: {str(e)}'}), 500

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")


@app.route('/sitemap.xml')
def serve_xml():
    return send_from_directory('static', 'sitemap.xml')

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)