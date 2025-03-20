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



# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)