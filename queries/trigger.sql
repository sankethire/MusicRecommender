create
or replace function trigger_add_recent_track() returns trigger as $body$ begin if (
  select
    count(*)
  from user_recent_tracks
  where
    user_recent_tracks.username = new.username
) >= 20 then begin
delete from user_recent_tracks
where
  new.username = user_recent_tracks.username
  and user_recent_tracks.time_stamp = (
    select
      min(time_stamp)
    from user_recent_tracks
    where
      new.username = user_recent_tracks.username
  );
end;
end if;
update user_interest_tags
set
  clicks = clicks + 1
where
  user_interest_tags.tag_name in (
    (
      select
        user_interest_tags.tag_name
      where
        user_interest_tags.username = new.username
    )
    intersect
      (
        select
          artist_tags.tag_name
        from artist_tags
        where
          artist_tags.artist_name = (
            select
              artist
            from songs
            where
              songs.uri = new.track_uri
          )
      )
  );
insert into user_interest_tags
select
  new.username,
  q1.tag_name,
  1
from (
    (
      select
        artist_tags.tag_name
      from artist_tags
      where
        artist_tags.artist_name = (
          select
            artist
          from songs
          where
            songs.uri = new.track_uri
        )
    )
    except
      (
        select
          user_interest_tags.tag_name
        from user_interest_tags
        where
          user_interest_tags.username = new.username
      )
  ) as q1;
return new;
end $body$ language plpgsql;


create trigger add_recent_track before
insert on user_recent_tracks for each row execute procedure trigger_add_recent_track();