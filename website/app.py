from flask import Flask, render_template, redirect, request
import psycopg2

# Connect to the database
db = 'host=10.17.50.126 dbname=group_18 user=group_18 password=604-287-987'
conn = psycopg2.connect(db)
cur = conn.cursor()

app = Flask(__name__, template_folder='template')


@app.route("/")
def login():
	
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
	print(pwd[0][0], password)
	if (pwd[0][0] == password):
		return pwd[0][0]
	else:
		return redirect("/")

if __name__ == "__main__":
	app.run(host="localhost", port=5001, debug=True)
	