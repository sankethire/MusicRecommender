-- potentially similar to interrested tags

-- artist with related tags but not influenced by clicks
select 
	*
from
	(select
	*
	from (
		select
		arts.artist_name,
		count(arts.artist_name)
		from (
			select
			artist_name
			from (
				select
				tag_name
				from user_interest_tags
				where
				username = 'yash98'
			) as in_tr,
			artist_tags
			where
			artist_tags.tag_name = in_tr.tag_name
		) as arts
		group by
		arts.artist_name
	) as arts_count
	order by
	count desc) as arts_desc,
	songs
where arts_desc.artist_name = songs.artist;

-- clicks based
select 
	*
from
	(select
	*
	from (
		select
		arts.artist_name,
		sum(arts.clicks)
		from (
			select
			artist_name, in_tr.tag_name, clicks
			from (
				select
				tag_name, clicks
				from user_interest_tags
				where
				username = 'yash98'
			) as in_tr,
			artist_tags
			where
			artist_tags.tag_name = in_tr.tag_name
		) as arts
		group by
		arts.artist_name) as arts_sum
	order by
	sum desc) as arts_desc,
	songs
where arts_desc.artist_name = songs.artist;

-- recent songs based tag or otherwise

select
  *
from (
    select
      *
    from (
        select
          arts.artist_name,
          count(arts.artist_name)
        from (
            select
              artist_name
            from (
            select
              artist_tags.tag_name
            from (
                select
                  songs.artist
                from (
                    select
                      track_uri
                    from user_recent_tracks
                    where
                      username = 'yash98'
                  ) as rt,
                  songs
                where
                  songs.uri = rt.track_uri
              ) as arts1,
              artist_tags
            where
              artist_tags.artist_name = arts.artist
          ) as arts
        group by
          arts.artist_name
      ) as arts_count
    order by
      count desc
  ) as arts_desc,
  songs
where
  arts_desc.artist_name = songs.artist;

-- New songs
