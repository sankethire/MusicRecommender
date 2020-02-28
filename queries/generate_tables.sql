\COPY artists FROM './csv/clean/artist_clean.csv' WITH CSV HEADER;

\COPY songs FROM './csv/clean/song_clean.csv' WITH CSV HEADER;

create table tags_temp(
  tag_id integer,
	tag_name text unique,
  freq integer,
  primary key(tag_name)
);

\COPY tags_temp FROM './csv/clean/tags_freq.csv' WITH CSV HEADER;

insert into tags(tag_name, freq) select tag_name, freq from tags_temp;

drop table tags_temp;

create table artist_tags_temp(
  artist_name text,
  tag_name text
);

\COPY artist_tags_temp FROM './csv/clean/artist_tags_1nf_clean.csv' WITH CSV HEADER;

insert into artist_tags(artist_name, tag_name)
select
  distinct artist_name,
  artist_tags_temp.tag_name
from artist_tags_temp, tags
where
  artist_tags_temp.tag_name is not null and
	tags.tag_name = artist_tags_temp.tag_name;

drop table artist_tags_temp;

drop table artists_raw;

drop table songs_raw;
