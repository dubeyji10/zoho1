
import os
import re
from flask import Flask
from flaskext.mysql import MySQL      # For newer versions of flask-mysql 
# from flask.ext.mysql import MySQL   # For older versions of flask-mysql
app = Flask(__name__)

mysql = MySQL()

mysql_database_host = 'MYSQL_DATABASE_HOST' in os.environ and os.environ['MYSQL_DATABASE_HOST'] or  'localhost'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'dubeyji'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'test_export_genius_2'
app.config['MYSQL_DATABASE_HOST'] = mysql_database_host
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
    return "Welcome!"

@app.route('/how are you')
def hello():
    return 'I am good, how about you?'

@app.route('/read from database')
def read():
    cursor.execute("SELECT * FROM employees")
    row = cursor.fetchone()
    result = []
    while row is not None:
      result.append(row[0])
      row = cursor.fetchone()

    return ",".join(result)

# @app.route('/ConnectToDatabase')
# def connecttodb():

@app.route('/ConnectToDatabase')
def dbConnection():
    with mysql.connect() as connectPointer:
        with connectPointer.cursor() as aCursor:
            print('connection established')
    
    return "connected to test_export_genius"


@app.route('/allclients')
def allclients():
    with mysql.connect() as connectPointer:
        print('connection established')
        with connectPointer.cursor() as aCursor:
            print('fetching clients')
            aCursor.execute('''SELECT * from clients''')
            result = aCursor.fetchall()

    return "connected to test_export_genius+clients total = {}".format(len(result))

if __name__ == "__main__":
    app.run()