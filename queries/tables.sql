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
  userid integer,
  username text unique,
  email text unique,
  passwd text,
  primary key (userid)
);

create table user_details(
  userid integer,
  first_name varchar(32),
  last_name varchar(32),
  primary key (userid),
  foreign key (userid) references users(userid) on delete cascade on update cascade
);

create table playlists(
  playlist_id integer,
  userid integer,
  primary key (playlist_id),
  foreign key (userid) references users(userid) on delete cascade on update cascade
);

create table playlist_tracks(
  playlist_id integer,
  track_uri varchar(36),
  primary key (playlist_id, track_uri),
  foreign key (playlist_id) references playlists(playlist_id) on delete cascade on update cascade,
  foreign key (track_uri) references songs(uri) on delete cascade on update cascade
);

create table user_interest_tags(
  userid integer,
  tag_name text,
  clicks integer,
  primary key (userid, tag_name),
  foreign key (userid) references users(userid) on delete cascade on update cascade,
  foreign key (tag_name) references tags(tag_name) on delete cascade on update cascade
);

create table user_recent_tracks(
  userid integer,
  track_uri varchar(36),
  time_stamp timestamp,
  primary key (userid, track_uri),
  foreign key (userid) references users(userid) on delete cascade on update cascade,
  foreign key (track_uri) references songs(uri) on delete cascade on update cascade
);
