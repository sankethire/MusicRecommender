create view clean_tags as(
  select
    distinct songs_raw.artist,
    artists_raw.tags_lastfm
  from songs_raw,
    artists_raw
  where
    songs_raw.artist = artists_raw.artist_lastfm
    and artists_raw.tags_lastfm is not null
    and artists_raw.ambiguous_artist != true
);

\copy (select * from clean_tags) to './csv/clean/artist_tags_clean.csv' delimiter ',' csv header;
