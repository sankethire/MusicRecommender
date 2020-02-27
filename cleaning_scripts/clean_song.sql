create view clean_song as 
(select
 songs_raw
from songs_raw, clean_tags
where
  clean_tags.artist = songs_raw.artist);

\copy (select * from clean_song) to 'song_clean.csv' delimiter ',' csv header;

drop view clean_song;
