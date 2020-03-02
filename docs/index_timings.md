project=# \timing 
Timing is on.

1) artist_country_index
    
	(a) index activate
	project=# select artist_name from artists where country = 'India';
	Time: 2.421 ms
	
	(b) index deactivate
	project=# select artist_name from artists where country = 'India';
	Time: 2.798 ms


2) artist_tag_index
   
	(a) index activate
	project=# select * from artist_tags where tag_name = 'rock';
	Time: 45.183 ms

	(b) index deactivate
	project=# select * from artist_tags where tag_name = 'rock';
	Time: 46.649 ms


3) track_artist_index

	Query 1:

		(a) index activate
		project=# select track, artist from songs where artist = 'AC/DC';
		(6 rows)

		Time: 7.187 ms

		(b) index deactivate
		project=# select track, artist from songs where artist = 'AC/DC';
		(6 rows)

		Time: 6.806 ms

	Query 2:
		(a) index activate
		project=# select track, artist from songs where artist = 'Taylor Swift';
		(49 rows)

		Time: 6.251 ms

		(b) index deactivate
		project=# select track, artist from songs where artist = 'Taylor Swift';
		(49 rows)

		Time: 6.768 ms

