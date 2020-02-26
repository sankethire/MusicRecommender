-- artist_raw table --
CREATE TABLE artists_raw(mbid VARCHAR,artist_mb VARCHAR,artist_lastfm VARCHAR,country_mb VARCHAR,country_lastfm VARCHAR,tags_mb VARCHAR,tags_lastfm VARCHAR,listeners_lastfm INTEGER,scrobbles_lastfm INTEGER,ambiguous_artist BOOLEAN);

SET CLIENT_ENCODING TO 'utf8';

 \COPY artists FROM '../csv/raw/artists/artists.csv' WITH CSV HEADER;

-- songs_raw table --
CREATE TABLE songs_raw(track VARCHAR,artist VARCHAR,uri VARCHAR,danceability DECIMAL,energy DECIMAL,key INTEGER,loudness DECIMAL,mode DECIMAL,speechiness DECIMAL,acousticness DECIMAL,instrumentalness DECIMAL,liveness DECIMAL,valence DECIMAL,tempo DECIMAL,duration_ms INTEGER,time_signature INTEGER,chorus_hit DECIMAL,sections INTEGER,target INTEGER);

SET CLIENT_ENCODING TO 'utf8';

\COPY songs FROM '../csv/raw/songs/dataset-of-00s.csv' WITH CSV HEADER;

\COPY songs FROM '../csv/raw/songs/dataset-of-60s.csv' WITH CSV HEADER;

\COPY songs FROM '../csv/raw/songs/dataset-of-70s.csv' WITH CSV HEADER;

\COPY songs FROM '../csv/raw/songs/dataset-of-80s.csv' WITH CSV HEADER;

\COPY songs FROM '../csv/raw/songs/dataset-of-90s.csv' WITH CSV HEADER;

\COPY songs FROM '../csv/raw/songs/dataset-of-10s.csv' WITH CSV HEADER;