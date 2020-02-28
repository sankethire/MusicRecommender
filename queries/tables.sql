create table artists(
  artist_name text ,
  country text,
  listeners integer,
  scrobbles integer,
  primary key (artist_name)
);

create table songs(
  track text,
  artist text,
  uri varchar(36),
  danceability decimal,
  energy decimal,
  track_key integer,
  loudness decimal,
  mode decimal,
  speechiness decimal,
  acousticness decimal,
  instrumentalness decimal,
  liveness decimal,
  valence decimal,
  tempo decimal,
  duration_ms integer,
  time_signature integer,
  chorus_hit decimal,
  sections integer,
  hit_target integer,
  primary key (uri),
  foreign key (artist) references artists(artist_name) on delete cascade on update cascade
);

create table tags(
  tag_name text unique,
  freq integer,
  primary key(tag_name)
);

create table artist_tags(
  artist_name text,
  tag_name text,
  primary key (artist_name, tag_name), 
  foreign key (artist_name) references artists(artist_name) on delete cascade on update cascade,
  foreign key (tag_name) references tags(tag_name) on delete cascade on update cascade
);

create table users(
  username text,
  email text unique,
  passwd text,
  primary key (username)
);

create table user_details(
  username text ,
  first_name varchar(32),
  last_name varchar(32),
  primary key (username),
  foreign key (username) references users(username) on delete cascade on update cascade
);

create table playlists(
  playlist_id integer,
  username text,
  playlist_name text,
  primary key (playlist_id),
  foreign key (username) references users(username) on delete cascade on update cascade
);

create table playlist_tracks(
  playlist_id integer,
  track_uri varchar(36),
  primary key (playlist_id, track_uri),
  foreign key (playlist_id) references playlists(playlist_id) on delete cascade on update cascade,
  foreign key (track_uri) references songs(uri) on delete cascade on update cascade
);

create table user_interest_tags(
  username text,
  tag_name text,
  clicks integer,
  primary key (username, tag_name),
  foreign key (username) references users(username) on delete cascade on update cascade,
  foreign key (tag_name) references tags(tag_name) on delete cascade on update cascade
);

create table user_recent_tracks(
  username text,
  track_uri varchar(36),
  time_stamp timestamp,
  primary key (username, track_uri),
  foreign key (username) references users(username) on delete cascade on update cascade,
  foreign key (track_uri) references songs(uri) on delete cascade on update cascade
);
