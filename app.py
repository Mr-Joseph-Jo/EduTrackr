from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enables frontend to call backend

app.secret_key = 'your_secret_key'

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'edutrackr'

mysql = MySQL(app)


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
            return redirect(url_for('admin_dashboard'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('adminlogin.html', msg=msg)

# Define the admin dashboard route
@app.route('/admin')
def admin_dashboard():
    if 'loggedin' in session:
        return render_template('admin.html')
    return redirect(url_for('admin_login'))

# Teacher Login Route
@app.route('/api/tlogin', methods=['POST'])
def teacher_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM teacher_login WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['loggedin'] = True
        session['username'] = user['username']
        return jsonify({'success': True, 'message': 'Login successful', 'username': user['username']})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
