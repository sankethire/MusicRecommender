# MusicRecommender
Music Recommendation System using postgres

## Datasets

- music artist popularity: https://www.kaggle.com/pieca111/music-artists-popularity
- the-spotify-hit-predictor-dataset: https://www.kaggle.com/theoverman/the-spotify-hit-predictor-dataset

## References

- Spotipy API: https://spotipy.readthedocs.io/en/2.9.0/#
- MusicBrainz API: https://python-musicbrainzngs.readthedocs.io/en/v0.7.1/

## Commands

1. Dump DB: `pg_dump -d project -h localhost -U postgres > project.sql`
2. Load DB: `psql -U postgres -d project -f project.sql` (Create DB named porject before hand)
