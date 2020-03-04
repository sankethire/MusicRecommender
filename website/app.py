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
	
	query = cur.execute(
	'''
	select 
		track, artist, uri
	from songs,
		(select
			*
		from (
			select
			arts.artist_name,
			sum(arts.clicks)
			from (
				select
				artist_name, in_tr.tag_name, clicks
				from (
					select
					tag_name, clicks
					from user_interest_tags
					where
					username = 'yash98'
				) as in_tr,
				artist_tags
				where
				artist_tags.tag_name = in_tr.tag_name
			) as arts
			group by
			arts.artist_name) as arts_sum
		order by
		sum desc
		limit 20) as arts_desc
	where arts_desc.artist_name = songs.artist 
	order by random();''')

	rows=cur.fetchall()

	track_info = []

	music_art = session.get('music_art')

	for row in rows[:20]:
		song_name = row[0]
		artist_name = row[1]
		uri = row[2]
		id_hash = uri.split(":")[-1]

		if music_art:
			track = sp.track(uri)
			# pprint(track)
			image_url = track['album']['images'][2]['url']

			track_info.append((uri, song_name, artist_name, id_hash, image_url))
		else:
			track_info.append((uri, song_name, artist_name, id_hash))

	return render_template('home.html', track_info=track_info, username=session.get('username'))

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
		session['music_art'] = False
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

@app.route('/toggle_music_art')
def toggle_music_art():
	if (session.get('music_art')):
		session['music_art'] = False
	else:
		session['music_art'] = True
	return ""

@app.route('/playlist')
def playlist():
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	"""
		select playlist_id, playlist_name from playlists where username = %s;
	""", (session.get('username'),))

	rows = cur.fetchall()

	playlists = []
	if len(rows) == 0:
		flash('You have no playlists')
	else:
		for playlist in rows:
			playlists.append((playlist[0], playlist[1]))
	
	return render_template('playlists.html', playlists=playlists)

@app.route('/add_playlist')
def add_playlist():
	if not session.get('logged_in'):
		return redirect('/login')

	return render_template('add_playlist.html')

@app.route('/add_playlist', methods=['POST'])
def add_playlist_to_table():
	if not session.get('logged_in'):
		return redirect('/login')

	playlist_name = request.form['playlist_name']

	# try:
	# 	query = cur.execute(
	# 	'''
	# 		insert into playlists (username, playlist_name) values(%s, %s);
	# 	''', (session.get('username'), playlist_name))
	# except Exception as e:
	# 	query1 = cur.execute(
	# 	'''
	# 		rollback;
	# 	''', (session.get('username'), playlist_name))
		
	# 	print(e)
	# 	flash('Playlist with name \'%s\' already exists' % (playlist_name,))
	# 	flash('Please choose another playlist name')

	# 	return render_template('add_playlist.html')
	# else:
	# 	query2 = cur.execute(
	# 	'''
	# 		commit;
	# 	''', (session.get('username'), playlist_name))
	
	query = cur.execute(
'''
	insert into playlists (username, playlist_name) values(%s, %s);
''', (session.get('username'), playlist_name))
	query2 = cur.execute(
'''
	commit;
''', (session.get('username'), playlist_name))

	return redirect('/playlist')

@app.route('/playlist/<playlist_id>')
def select_playlist(playlist_id):
	if not session.get('logged_in'):
		return redirect('/login')

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

	music_art = session.get('music_art')

	for track in rows1:
		id_hash = track[0].split(":")[-1]

		if music_art:
			track_s = sp.track(track[0])
			# pprint(track)
			image_url = track_s['album']['images'][2]['url']

			playlist_tracks.append((track[0], track[1], track[2], id_hash, image_url))
		else:
			playlist_tracks.append((track[0], track[1], track[2], id_hash))

	if len(playlist_tracks) == 0:
		flash('Playlist is empty')

	return render_template('playlist_tracks.html', playlist_name=rows[0][1], playlist_tracks=playlist_tracks)

@app.route('/songs/<track_uri>')
def songs(track_uri):
	if not session.get('logged_in'):
		return redirect('/login')

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

	return render_template('songs.html', song_name=song_name, artist_name=artist_name, image_url=image_url, uri=uri)

@app.route('/songs/<track_uri>/play')
def play_song(track_uri):
	if not session.get('logged_in'):
		return redirect('/login')

	try:
		query = cur.execute(
		'''
			insert into user_recent_tracks values(%s, %s, now());
		''', (session.get('username'), track_uri))
	except Exception as e:
		query1 = cur.execute('''
		rollback;
		''')

		print(e)
	else:
		query2 = cur.execute('''
		commit;
		''')

	return ""

@app.route('/songs/<track_uri>/add_to_playlist')
def adding_playlist(track_uri):
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	"""
		select playlist_id, playlist_name from playlists where username = %s;
	""", (session.get('username'),))

	rows = cur.fetchall()

	playlists = []
	if len(rows) == 0:
		flash('You have no playlists')
	else:
		for playlist in rows:
			playlists.append((playlist[0], playlist[1]))
	
	return render_template('add_to_playlist.html', playlists=playlists)


@app.route('/songs/<track_uri>/add_to_playlist/<playlist_id>')
def add_to_playlist(track_uri, playlist_id):
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	"""
		select username, playlist_name from playlists where playlist_id = %s;
	""", (playlist_id,))

	rows = cur.fetchall()

	if rows[0][0] != session.get('username'):
		# TODO: alert message here
		redirect('/home')

	try:
		query = cur.execute('''
		insert into playlist_tracks values(%s, %s);
		''', (playlist_id, track_uri))
	except psycopg2.errors.UniqueViolation as uniq_voil:
		query1 = cur.execute('''
		rollback;
		''')
		# TODO: display reason of error song already exists in playlist
	else:
		query2 = cur.execute('''
		commit;
		''')

	return redirect('/playlist/'+str(playlist_id))

@app.route('/songs/<track_uri>/delete_from_playlist/<playlist_id>')
def delete_from_playlist(track_uri, playlist_id):
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	"""
		select username, playlist_name from playlists where playlist_id = %s;
	""", (playlist_id,))

	rows = cur.fetchall()

	if rows[0][0] != session.get('username'):
		# TODO: alert message here
		redirect('/home')

	try:
		query = cur.execute('''
		delete from playlist_tracks where playlist_id = %s and track_uri = %s;
		''', (playlist_id, track_uri))
	except psycopg2.errors.UniqueViolation as uniq_voil:
		query1 = cur.execute('''
		rollback;
		''')
		# TODO: display reason of error song already exists in playlist
	else:
		query2 = cur.execute('''
		commit;
		''')

	return redirect('/playlist/'+str(playlist_id))


@app.route('/delete_playlist/<playlist_id>')
def delete_playlist(playlist_id):
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	"""
		select username, playlist_name from playlists where playlist_id = %s;
	""", (playlist_id,))

	rows = cur.fetchall()

	try:
		query = cur.execute('''
		delete from playlists where playlist_id = %s;
		''', (playlist_id,))
	except Exception as e:
		query1 = cur.execute('''
		rollback;
		''')
		print(e)
	else:
		query2 = cur.execute('''
		commit;
		''')
	
	return redirect('/playlist')

@app.route('/search')
def search():
	if not session.get('logged_in'):
		return redirect('/login')

	return render_template("search.html")

@app.route('/search', methods=['POST'])
def search_query():
	if not session.get('logged_in'):
		return redirect('/login')

	song_name = request.form['song_name']
	artist_name = request.form['artist_name']

	query_str = "select * from songs "
	if song_name == '' and artist_name == '':
		return redirect('/search')
	if song_name != '':
		query_str += 'where '
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

	if len(rows) == 0:
		flash('No results found')

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


@app.route('/profile')
def profile():
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	"""
		select users.username,first_name,last_name, email, passwd from users, user_details where users.username = user_details.username and users.username = %s;
	""", (session.get('username'),))
	userdetail = cur.fetchall()

	# print(userdetail)
	return render_template('profile.html',userdetail=userdetail[0])

@app.route('/profile/interests')
def interest():
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	'''
		select tag_name, clicks from user_interest_tags where username = %s order by clicks desc;
	''', (session.get('username'),) )

	interests = cur.fetchall()

	return render_template('user_interests.html', interests=interests)

@app.route('/recent_tracks')
def recent_tracks():
	if not session.get('logged_in'):
		return redirect('/login')

	query = cur.execute(
	'''
		select track_uri, track, time_stamp from user_recent_tracks, songs where username = %s and uri = track_uri order by time_stamp desc;
	''', (session.get('username'),) )

	track_times = cur.fetchall()

	return render_template('recent_tracks.html', track_times=track_times)

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host="localhost", port=5001, debug=True)
	