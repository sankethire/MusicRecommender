.phony: artists.csv

artists.csv:
	cd csv/raw/artists && rm -f artists.csv && cat artists*.csv > artists.csv && wc -l artists.csv