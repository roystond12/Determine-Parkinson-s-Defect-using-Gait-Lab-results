from flask import Flask, request, render_template, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from second import second
from Pose_details import pose_details
from stream import stream

app = Flask(__name__)  
app.register_blueprint(second)
app.register_blueprint(pose_details)
app.register_blueprint(stream)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'users'
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/video', methods=['GET']) 
def video():
    return render_template("video.html")

@app.route('/login', methods=['POST']) 
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
    account = cursor.fetchone()
    if account:
        return render_template("index.html") + '<script>alert("Login successful")</script>'
    else:
        return render_template('login.html') + '<script>alert("Login unsuccessful. Please try again.")</script>'

@app.route('/enter_data', methods=['GET'])
def enter_data():
    print("enter_data function executed")
    return render_template("enter_data.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)

