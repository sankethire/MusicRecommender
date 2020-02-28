\COPY artists FROM './csv/clean/artist_clean.csv' WITH CSV HEADER;

\COPY songs FROM './csv/clean/song_clean.csv' WITH CSV HEADER;

\COPY tags FROM './csv/clean/tags_freq.csv' WITH CSV HEADER;

\COPY artist_tags FROM './csv/clean/artist_tags_1nf_clean.csv' WITH CSV HEADER;
