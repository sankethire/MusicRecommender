# Tables

```sql
1. users(userid, username, email, password)
2. user_details(userid, first_name, last_name)
3. playlists(playlist_id, userid, visibility)
4. playlist_tracks(playlist_id, track_uri)
5. songs(track TEXT,artist TEXT,uri TEXT,danceability DECIMAL,energy DECIMAL,key INTEGER,loudness DECIMAL,mode DECIMAL,speechiness DECIMAL,acousticness DECIMAL,instrumentalness DECIMAL,liveness DECIMAL,valence DECIMAL,tempo DECIMAL,duration_ms INTEGER,time_signature INTEGER,chorus_hit DECIMAL,sections INTEGER,target INTEGER)
6. artists(mbid TEXT,artist_mb TEXT,artist_lastfm TEXT,country_mb TEXT,country_lastfm TEXT,tags_mb TEXT,tags_lastfm TEXT,listeners_lastfm INTEGER,scrobbles_lastfm INTEGER,ambiguous_artist BOOLEAN)
7. user_interest_tags(userid, tag_id, clicks)
	- clicks: number of times user was interested in a tag
8. tags(tag_id, tag_name, freq)
9. user_recent_tracks(userid, track_uri)
```
