create view clean_song as 
(select
 songs
from songs, clean_tags
where
  clean_tags.artist = songs.artist);

\copy (select * from clean_song) to 'song_clean.csv' delimiter ',' csv header;

drop view clean_song;
