<<<<<<< HEAD
create index artist_name_index on artists(artist_name);

create index track_index on songs(track);
=======
create index artist_country_index on artists using brin(country);

create index track_artist_index on songs using brin(artist);

create index artist_tag_index on artist_tags using brin(tag_name);
>>>>>>> 69e66e58cd505f9037bf75969f087ca39bb3625d
