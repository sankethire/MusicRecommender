# Ideas

## Assumption
- User fabricated data

## Tables

## User

- Search History
- Save playlist
- Searching Filtering

## Front Page

- Buttons
  - login
  - register
- Info/feature

## Playlist

- Global
  - Public or Private (User associated)
- <del> request access </del>
  - <del> User sends request to other user </del>

## Spotipy
### Playing songs

- using spotipy API
- showcasing image

## Recomdations

### Random Selection

- calculate running avg and stdev
- random selection excluding already listened

### Playlist (most likely bad idea)

- playlist of songs with similar values
- Recommending playlists instead
- will have to club playlist before hand

### Artist tags based selection (selected since we only have artist tags)

- save tags user is interested in based on tags from artist of songs they listened to
- select another artist based on the tag recomend thats artists song to them


## Queries

1. User login authentication
2. Save / View playlists
3. Search related (e.g search by some attribute)
4. recommendation system
5. saving song history of user
6. Access to user to -> update the song and artist database by adding new song -> keeping track of updations using triggers.
7. Access to user to add a tag to song if he/she wants to (track by trigger).

- In 6 and 7, user's updations (as a trigger log) will be visible to admin, so that admin can review updation and make a decision to either keep the updation as it is (delete that particular updation log)  or restore the updation into the database.

# todo in end
1. Recursive queries tag - tag connection