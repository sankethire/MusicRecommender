from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import psycopg2
import os

# Connect to the database
db = 'host=localhost dbname=project user=postgres password=postgres'
conn = psycopg2.connect(db)
cur = conn.cursor()

app = Flask(__name__, template_folder='template')

@app.route("/")
def home():
	if not session.get('logged_in'):
		return render_template("login.html")
	else:
		return "Yo " + session['username']

@app.route('/', methods=['POST'])
def authenticate():
	username = request.form['username']
	password = request.form['password']

	cur.execute(
	"""
		select passwd from users where username = %s;
	""", (username,))

	pwd = cur.fetchall()

	if (len(pwd) == 0):
		flash('Invalid username or password')
		return home()
	elif (pwd[0][0] == password):
		session['logged_in'] = True
		session['username'] = username
		return home()
	else:
		flash('Invalid username or password')
		return home()

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def createuser():
	
	username = request.form['username']
	password = request.form['password']
	firstname = request.form['firstname']
	lastname = request.form['lastname']
	email = request.form['email']

	try:
		query = cur.execute(
		"""
			insert into users values(%s, %s, %s);
		""", (username, email, password))
	except psycopg2.errors.UniqueViolation as uniq_voil:
		query1 = cur.execute(
		"""
			rollback;
		""")

		for arg in uniq_voil.args:
			if "users_pkey" in arg:
				flash('Username already exists')
				flash('Pick a different username')

			if "users_email_key" in arg:
				flash('Email already exists')
		return signup()
	else:
		query2 = cur.execute(
		"""
			commit;
		""")

	query = cur.execute(
	"""
		insert into user_details values(%s, %s, %s);
	""", (username, firstname, lastname))

	return home()


@app.route('/login.html')
def login():
	return render_template('login.html')


def get_query_tuples(query):
	cur.execute(query)
	header = [i[0] for i in cur.description]
	rows = [list(i) for i in cur.fetchall()]
	# print("------------------------------")
	# print(len(rows))
	rows.insert(0,header)
	return rows

def tuples_to_html(tuples):
	htable=''
	tuples[0] = ['<b>' + i.upper() + '</b>' for i in tuples[0]] 
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


@app.route('/table.html')
def a():
	query = """select track from songs where artist = 'AC/DC'"""
	# with open('table.html', 'w') as filetowrite:
	# 	filetowrite.write(query_to_html(query))
	# return render_template('table.html')
	return render_template('table.html', table=query_to_html(query))

@app.route('/home.html')
def b():
	return render_template('home.html')

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host="localhost", port=5001, debug=True)
	