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
            df.columns = df.columns.str.strip().str.lower()

            print(df.head())  # Debugging: Print the first few rows

            required_columns = {'uid', 'batch', 'semester_id', 'semester_name', 'name'}
            if not required_columns.issubset(df.columns):
                return jsonify({'message': 'Missing required columns in the file'}), 400

            cursor = mysql.connection.cursor()

            duplicate_uids = set()
            for index, row in df.iterrows():
                print("Processing Row:", row.to_dict())  # Debugging line

                semester_id = row.get('semester_id')
                if pd.isna(semester_id) or not isinstance(semester_id, (int, float)):
                    return jsonify({'message': f'Invalid Semester ID at row {index + 2}'}), 400

                semester_id = int(semester_id)

                cursor.execute('SELECT * FROM sem WHERE semester_id = %s', (semester_id,))
                semester = cursor.fetchone()
                if not semester:
                    return jsonify({'message': f'Semester ID {semester_id} does not exist'}), 400

                table_map = {1: 's1', 2: 's2', 3: 's3', 4: 's4', 5: 's5', 6: 's6', 7: 's7', 8: 's8'}
                table_name = table_map.get(semester_id)
                if not table_name:
                    return jsonify({'message': f'Invalid semester ID {semester_id}'}), 400
                # **Ensure correct column names for each semester**
                column_mappings = {
                    "s1": [
                        'uid', 'batch', 'semester_id', 'semester_name', 'name',
                        'lac_marks', 'lac_grade', 'engg_chem_marks', 'engg_chem_grade', 
                        'engg_graphics_marks', 'engg_graphics_grade', 'basics_ce_me_marks', 
                        'basics_ce_me_grade', 'ls_marks', 'ls_grade', 'chem_lab_marks', 
                        'chem_lab_grade', 'workshop_marks', 'workshop_grade', 'sgpa', 'cgpa'
                    ],
                    "s2": [
                        'uid', 'batch', 'semester_id', 'semester_name', 'name',
                        'vector_calculus_marks', 'vector_calculus_grade', 'engg_physics_marks', 
                        'engg_physics_grade', 'engg_mechanics_marks', 'engg_mechanics_grade', 
                        'professional_communication_marks', 'professional_communication_grade', 
                        'basics_of_electronic_and_electricals_marks', 'basics_of_electronic_and_electricals_grade', 
                        'programming_in_c_marks', 'programming_in_c_grade', 'engg_physics_lab_marks', 
                        'engg_physics_lab_grade', 'electrical_electronic_lab_mark', 'electrical_electronic_lab_grade', 
                        'sgpa', 'cgpa'
                    ],
                    "s3": [
                        'uid', 'batch', 'semester_id', 'semester_name', 'name',
                        'dms_marks', 'dms_grade', 'ds_marks', 'ds_grade', 
                        'dsd_marks', 'dsd_grade', 'python_marks', 'python_grade', 
                        'design_and_engineering_marks', 'design_and_engineering_grade', 
                        'sustainable_engineering_marks', 'sustainable_engineering_grade', 
                        'ds_lab_marks', 'ds_lab_grade', 'python_lab_mark', 'python_lab_grade', 
                        'sgpa', 'cgpa'
                    ],
                    "s4": [
                        'uid', 'batch', 'semester_id', 'semester_name', 'name',
                        'principles_of_object_oriented_techniques_marks', 'principles_of_object_oriented_techniques_grade',
                        'graph_theory_marks', 'graph_theory_grade',
                        'computer_organization_marks', 'computer_organization_grade',
                        'database_management_systems_marks', 'database_management_systems_grade',
                        'professional_ethics_marks', 'professional_ethics_grade',
                        'constitution_of_india_marks', 'constitution_of_india_grade',
                        'object_oriented_techniques_lab_marks', 'object_oriented_techniques_lab_grade',
                        'database_management_systems_lab_marks', 'database_management_systems_lab_grade',
                        'sgpa', 'cgpa'
                    ],
                    "s5": [
                        'uid', 'batch', 'semester_id', 'semester_name', 'name',
                        'web_application_development_marks', 'web_application_development_grade',
                        'operating_system_concepts_marks', 'operation_system_concepts_grade',
                        'data_communication_and_networking_marks', 'data_communication_and_networking_grade',
                        'formal_languages_and_automata_theory_marks', 'formal_languages_and_automata_theory_grade',
                        'management_for_software_engineers_marks', 'management_for_software_engineers_grade',
                        'disaster_management_marks', 'disaster_management_grade',
                        'operating_system_and_network_programming_lab_marks', 'operating_system_and_network_programming_lab_grade',
                        'web_application_development_lab_marks', 'web_application_development_lab_grade',
                        'sgpa', 'cgpa'
                    ],
                    "s6": [
                        'uid', 'batch', 'semester_id', 'semester_name', 'name',
                        'internetworking_with_tcp_ip_marks', 'internetworking_with_tcp_ip_grade',
                        'algorithm_analysis_and_design_marks', 'algorithm_analysis_and_design_grade',
                        'data_science_marks', 'data_science_grade',
                        'soft_computing_marks', 'soft_computing_grade',
                        'digital_image_processing_marks', 'digital_image_processing_grade',
                        'industrial_economics_and_foreign_trade_marks', 'industrial_economics_and_foreign_trade_grade',
                        'computer_networks_lab_marks', 'computer_networks_lab_grade',
                        'miniproject_marks', 'miniproject_grade',
                        'sgpa', 'cgpa'
                    ],
                    "s7": [
                        "uid", "batch", "semester_id", "semester_name", "name",
                        "data_analytics_marks", "data_analytics_grade",
                        "mobile_computing_marks", "mobile_computing_grade",
                        "artificial_intelligence_marks", "artificial_intelligence_grade",
                        "industrial_safety_engineering_marks", "industrial_safety_engineering_grade",
                        "data_analytics_lab_marks", "data_analytics_lab_grade",
                        "seminar_marks", "seminar_grade",
                        "project_phase1_marks", "project_phase1_grade",
                        "sgpa", "cgpa"
                    ],
                    "s8": [
                        "uid", "batch", "semester_id", "semester_name", "name",
                        "cryptography_and_network_security_marks", "cryptography_and_network_security_grade",
                        "computer_vision_marks", "computer_vision_grade",
                        "cloud_computing_marks", "cloud_computing_grade",
                        "internet_of_things_marks", "internet_of_things_grade",
                        "adhoc_and_wireless_sensor_networks_marks", "adhoc_and_wireless_sensor_networks_grade",
                        "software_architecture_marks", "software_architecture_grade",
                        "natural_language_processing_marks", "natural_language_processing_grade",
                        "project_phase2_marks", "project_phase2_grade",
                        "sgpa", "cgpa"
                    ]

                }


                duplicate_uids = set()
            for index, row in df.iterrows():
                print("Processing Row:", row.to_dict())  # Debugging line

                semester_id = row.get('semester_id')
                if pd.isna(semester_id) or not isinstance(semester_id, (int, float)):
                    return jsonify({'message': f'Invalid Semester ID at row {index + 2}'}), 400

                semester_id = int(semester_id)

                # Check if semester ID exists in the database
                cursor.execute('SELECT * FROM sem WHERE semester_id = %s', (semester_id,))
                semester = cursor.fetchone()
                if not semester:
                    return jsonify({'message': f'Semester ID {semester_id} does not exist'}), 400

                # Determine the table name and column structure
                table_name = table_map.get(semester_id)
                if not table_name or table_name not in column_mappings:
                    return jsonify({'message': f'Invalid semester ID or table name {semester_id}'}), 400

                columns = column_mappings[table_name]

                # Check for duplicate `uid` in the corresponding table
                uid = row.get('uid')
                cursor.execute(f'SELECT * FROM {table_name} WHERE uid = %s', (uid,))
                if cursor.fetchone():
                    duplicate_uids.add(uid)
                    continue  # Skip duplicate rows

                # Clean up and preprocess numeric fields
                for col in df.columns:
                    if "marks" in col.lower() or "sgpa" in col.lower() or "cgpa" in col.lower():
                        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric to NaN
                        df[col] = df[col].fillna(0)  # Fill NaN with 0

                # Prepare and execute the insert query
                query = f'''
                    INSERT INTO {table_name} ({', '.join(columns)}) 
                    VALUES ({', '.join(['%s'] * len(columns))})
                '''
                values = tuple(row[col] for col in columns)
                cursor.execute(query, values)

            if duplicate_uids:
                print("Duplicate UIDs Found:", duplicate_uids)  # Debugging: List duplicate UIDs

            mysql.connection.commit()
            cursor.close()
            return jsonify({
                'message': 'File successfully uploaded and database updated',
                'duplicates': list(duplicate_uids)
            }), 200

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