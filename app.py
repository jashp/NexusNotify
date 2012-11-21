from flask import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', name=None)

@app.route('/add', methods=['POST'])
def add():
    return "OK"


if __name__ == '__main__':
    app.run()