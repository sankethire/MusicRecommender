create index artist_country_index on artists using brin(country);

create index track_artist_index on songs using brin(artist);

create index artist_tag_index on artist_tags using brin(tag_name);
