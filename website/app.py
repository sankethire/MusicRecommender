from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import psycopg2
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

from pprint import pprint

# Connect to the database
db = 'host=localhost dbname=project user=postgres password=postgres'
conn = psycopg2.connect(db)
cur = conn.cursor()

app = Flask(__name__)

def check_loggedin():
	if not session.get('logged_in'):
		return redirect('/login')
	else:
		return redirect('/home')

@app.route('/')
def root():
	return check_loggedin()

@app.route('/home')
def home():
	if not session.get('logged_in'):
		return redirect('/login')
	else:
		return render_template('home.html')

@app.route('/login')
def login():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return redirect('/home')

@app.route('/login', methods=['POST'])
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
		return redirect('/home')
	elif (pwd[0][0] == password):
		session['logged_in'] = True
		session['username'] = username
		return redirect('/home')
	else:
		flash('Invalid username or password')
		return redirect('/home')

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

	return redirect('/home')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('login')

@app.route('/playlist')
def playlist():
	query = cur.execute(
	"""
		select playlist_id, playlist_name from playlists where username = %s;
	""", (session.get('username'),))

	rows = cur.fetchall()

	playlists = []
	for playlist in rows:
		playlists.append(("/playlist/" + str(playlist[0]), playlist[1]))
	return render_template('playlists.html', playlists=playlists)

@app.route('/playlist/<playlist_id>')
def select_playlist(playlist_id):
	query = cur.execute(
	"""
		select username, playlist_name from playlists where playlist_id = %s;
	""", (playlist_id,))

	rows = cur.fetchall()

	if rows[0][0] != session.get('username'):
		# TODO: alert message here
		redirect('/home')

	query1 = cur.execute(
	"""
		select track_uri, track, artist from playlist_tracks, songs where playlist_id = %s and track_uri = uri;
	""", (playlist_id,))

	rows1 = cur.fetchall()

	playlist_tracks = []

	for track in rows1:
		playlist_tracks.append(("/songs/"+track[0], track[1], track[2]))

	return render_template('playlist_tracks.html', playlist_name=rows[0][1], playlist_tracks=playlist_tracks)

@app.route('/songs/<track_uri>')
def songs(track_uri):
	query = cur.execute(
	"""
		select * from songs where uri = %s;
	""", (track_uri,))

	rows = cur.fetchall()

	song_name = rows[0][0]
	artist_name = rows[0][1]
	uri = rows[0][2]

	track = sp.track(uri)

	# pprint(track)

	image_url = track['album']['images'][1]['url']

	return render_template('songs.html', song_name=song_name, artist_name=artist_name, image_url=image_url)

@app.route('/search')
def search():
	return render_template("search.html")

@app.route('/search', methods=['POST'])
def search_query():
	song_name = request.form['song_name']
	artist_name = request.form['artist_name']

	query_str = "select * from songs "
	if song_name == '' and artist_name == '':
		return redirect('/search')
	else:
		query_str += 'where '
	if song_name != '':
		query_str += 'track ~* \'%s\' ' % song_name
	if artist_name != '':
		if 'where ' in query_str:
			query_str += 'and '
		else:
			query_str += 'where '

		query_str += 'artist ~* \'%s\' ' % artist_name
	query_str += ';'

	query = cur.execute(query_str)
	rows = cur.fetchall()


	return render_template('search.html', rows=rows)

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

def query_to_html(query=None, rows=[], to_execute=False):
	if to_execute:
		cur.execute(query)
	header = [i[0] for i in cur.description]
	rows = [list(i) for i in cur.fetchall()]
	rows.insert(0,header)
	return tuples_to_html(rows)

@app.route('/table.html')
def a():
	query = """select track from songs where artist = 'AC/DC'"""
	# with open('table.html', 'w') as filetowrite:
	# 	filetowrite.write(query_to_html(query))
	# return render_template('table.html')
	return render_template('table.html', table=query_to_html(query, to_execute=True))


@app.route('/navbar.html')
def navbar():
	return render_template('navbar.html')

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host="localhost", port=5001, debug=True)
	