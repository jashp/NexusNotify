from flask import *
import MySQLdb
from local_settings import *

app = Flask(__name__)
db = MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASS,db=DB_NAME)

@app.route('/')
def hello_world():
    return render_template('index.html', name=None)

@app.route('/add', methods=['POST'])
def add():
	versions = request.form.getlist("inputVersion[]")
	email = request.form["inputEmail"]
	location = request.form["inputLocation"]
	num_versions = len(versions)
	c = db.cursor()
	c.executemany("INSERT INTO emails (email, location, version) VALUES (%s, %s,%s) ON DUPLICATE KEY UPDATE sent=0, unsubscribe=0", zip([email]*num_versions, [location]*num_versions, versions))
	db.commit()
	return "OK"


if __name__ == '__main__':
    app.run()