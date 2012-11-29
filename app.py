from flask import *
import MySQLdb
from local_settings import *
from recaptcha import *
from flask_wtf import Form, RecaptchaField
from wtforms import *
from wtforms.validators import *
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config["RECAPTCHA_PUBLIC_KEY"] = RECAPTCHA_PUBLIC_KEY
app.config["RECAPTCHA_PRIVATE_KEY"] = RECAPTCHA_PRIVATE_KEY
app.debug = DEBUG
csrf = CsrfProtect()
db = MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASS,db=DB_NAME)

class AddForm(Form):
	email = TextField('email', validators=[Required(), Email()])
	location = SelectField('location', choices=[('0', 'United States'), ('1', 'Canada')], validators=[Required()])
	versions = SelectMultipleField('versions', choices=[('0', 'Nexus 4 (8gb)'), ('1', 'Nexus 4 (16gb)')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False) , validators=[Required()])
	if not app.debug:
		recaptcha = RecaptchaField()
		
@app.route('/')
def hello_world():
	form = AddForm()
	return render_template('index.html', form=form, debug=app.debug)

@csrf.exempt
@app.route('/add', methods=['POST'])
def add():
	form = AddForm(request.form)
	if not form.validate():
		abort(400)

	versions = form.versions.data
	email = form.email.data
	location = form.location.data
	num_versions = len(versions)
	c = db.cursor()
	c.executemany("INSERT INTO emails (email, location, version) VALUES (%s, %s,%s) ON DUPLICATE KEY UPDATE sent=0, unsubscribe=0", zip([email]*num_versions, [location]*num_versions, versions))
	db.commit()
	return "OK"

@app.route('/unsubscribe', methods=["POST"])
def remove():
	email = request.form["inputEmail"]
	c = db.cursor()
	c.execute("UPDATE emails SET unsubscribe=1 WHERE email = %s", email)
	db.commit()
	return "OK"

if __name__ == '__main__':
	app.run()