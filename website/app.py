from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import psycopg2
import os

# Connect to the database
db = 'host=10.17.50.126 dbname=group_18 user=group_18 password=604-287-987'
conn = psycopg2.connect(db)
cur = conn.cursor()

app = Flask(__name__, template_folder='template')

@app.route("/")
def home():
	if not session.get('logged_in'):
		return render_template("login.html")

@app.route('/', methods=['POST'])
def authenticate():
	username = request.form['username']
	password = request.form['password']

	cur.execute(
	"""
		select passwd from users where username = %s
	""", (username,))

	pwd = cur.fetchall()

	if (pwd[0][0] == password):
		session['logged_in'] = True
		session['username'] = username
	else:
		flash('Invalid username or password')
		return home()

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host="localhost", port=5001, debug=True)
	