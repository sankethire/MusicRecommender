.phony: raw_table

raw_table:
	sudo -u postgres psql $(PG_PROJECT) $(PG_USER) -f cleaning_scripts/clean_artist_tags.sql

csv/raw/artists/artists.csv:
	cd csv/raw/artists && rm -f artists.csv && cat artists*.csv > artists.csv && wc -l artists.csv