create or replace function trigger_add_recent_track()
	returns trigger as 
	$body$
		begin
			if (select count(*) from user_recent_tracks where user_recent_tracks.username = new.username) = 10 then
				begin
					delete from user_recent_tracks using (select * from user_recent_tracks where new.username = user_recent_tracks.username) as q1 where q1.time_stamp = min(time_stamp);
				end;
			end if;
		end
	$body$
language plpgsql;

create trigger add_recent_track
	before insert
	on user_recent_tracks
	for each row
	execute procedure trigger_add_recent_track();

-- create function trigger_add_recent_track()
-- 	returns trigger as 
-- 	$body$
-- 		begin
-- 			if (select count(*) from user_recent_tracks where user_recent_tracks.username = new.username) < 10 then
-- 				begin
-- 					insert into user_recent_tracks values(new.*);
-- 				end;
-- 			else 
-- 				begin
-- 					update user_recent_tracks set track_uri = new.track_uri, time_stamp = now() from (select * from user_recent_tracks where new.username = user_recent_tracks.username) as q1 where q1.time_stamp = min(time_stamp);
-- 				end;
-- 			end if;
-- 		end
-- 	$body$
-- language plpgsql;