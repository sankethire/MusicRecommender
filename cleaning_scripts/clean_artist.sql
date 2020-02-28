create view clean_artist as 
(select
  distinct artists_raw.artist_lastfm,
  artists_raw.country_lastfm,
  artists_raw.listeners_lastfm,
  artists_raw.scrobbles_lastfm
from artists_raw, clean_tags
where
  clean_tags.artist = artists_raw.artist_lastfm);

\copy (select * from clean_artist) to './csv/clean/artist_clean.csv' delimiter ',' csv header;

drop view clean_artist;