create view clean_artist as 
(select
  distinct artists.artist_lastfm,
  artists.country_lastfm,
  artists.listeners_lastfm,
  artists.scrobbles_lastfm
from artists, clean_tags
where
  clean_tags.artist = artists.artist_lastfm);

\copy (select * from clean_artist) to 'artist_clean.csv' delimiter ',' csv header;

drop view clean_artist;