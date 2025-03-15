from flask import Flask, request, render_template, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'users'
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST']) 
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
    account = cursor.fetchone()
    if account:
        return render_template("index.html") + '<script>alert("Login successful")</script>'
    else:
        return render_template('login.html') + '<script>alert("Login unsuccessful. Please try again.")</script>'
    
@app.route('/enter_data', methods=['GET'])
def enter_data():
    return render_template("enter_data.html")
if __name__ == '__main__':
    app.run(debug=True,port=5000)

