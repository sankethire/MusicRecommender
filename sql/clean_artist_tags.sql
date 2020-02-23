create view clean_tags as(
  select
    distinct songs.artist,
    artists.tags_lastfm
  from songs,
    artists
  where
    songs.artist = artists.artist_lastfm
    and artists.tags_lastfm is not null
    and artists.ambiguous_artist != true
);

\copy (select * from clean_tags) to 'artist_tags_clean.csv' delimiter ',' csv header;
