from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'dubeyji'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'test_export_genius'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)