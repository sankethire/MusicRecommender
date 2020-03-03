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

@app.route('/table.html')
def table():

	def get_query_tuples(query):
		cur.execute(query)
		header = [i[0] for i in cur.description]
		rows = [list(i) for i in cur.fetchall()]
		rows.insert(0,header)
		return rows

	def tuples_to_html(tuples):
		htable='<table border="1" bordercolor=000000 cellspacing="0" cellpadding="1" style="table-layout:fixed;vertical-align:bottom;font-size:13px;font-family:verdana,sans,sans-serif;border-collapse:collapse;border:1px solid rgb(130,130,130)" >'
		tuples[0] = ['<b>' + i + '</b>' for i in tuples[0]] 
		for row in tuples:
			new_row = '<tr>' 
			new_row += '<td align="left" style="padding:1px 4px">'+ str(row[0])+'</td>'
			row.remove(row[0])
			new_row = new_row + ''.join(['<td align="right" style="padding:1px 4px">' + str(x) + '</td>' for x in row])  
			new_row += '</tr>' 
			htable+= new_row
		htable += '</table>'
		return htable

	def query_to_html(query):
		return tuples_to_html(get_query_tuples(query))


	query = """select track from songs where artist = 'AC/DC'"""
	with open('table.html', 'w') as filetowrite:
		filetowrite.write(query_to_html(query))
	return render_template('table.html')

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host="localhost", port=5001, debug=True)
	