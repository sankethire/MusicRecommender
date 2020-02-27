create table users(userid integer unique, username text unique, email text unique, passwd text, primary key (userid));

create table user_details(userid integer unique, first_name varchar(32), last_name varchar(32), primary key (userid));

create table playlists(playlist_id integer unique, userid integer, primary key (playlist_id, userid));

create table playlist_tracks(playlist_id integer unique, track_uri varchar(36), primary key (playlist_id));

create table songs(track text, artist text, uri varchar(36), danceability decimal, energy decimal, track_key integer, loudness decimal, mode decimal, speechiness decimal, acousticness decimal, instrumentalness decimal, liveness decimal, valence decimal, tempo decimal, duration_ms integer, time_signature integer, chorus_hit decimal, sections integer, hit_target integer);

create table artists(mbid varchar(37), artist_name text, country text, listeners integer, scrobbles integer);

create table user_interest_tags(userid integer, tag_id integer, clicks integer);

create table tags(tag_id integer, tag_name text, freq integer);

create table artist_tags(mbid varchar(37), tag_id integer);

create table user_recent_tracks(userid integer, track_uri varchar(36), time_stamp timestamp);
