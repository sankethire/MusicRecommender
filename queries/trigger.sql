create or replace function trigger_add_recent_track()
	returns trigger as 
	$body$
		begin
			if (select count(*) from user_recent_tracks where user_recent_tracks.username = new.username) >= 10 then
				begin
					delete from user_recent_tracks where new.username = user_recent_tracks.username and user_recent_tracks.time_stamp = (select min(time_stamp) from user_recent_tracks where new.username = user_recent_tracks.username);
				end;
			end if;
			return new;
		end
	$body$
language plpgsql;

create trigger add_recent_track
	before insert
	on user_recent_tracks
	for each row
	execute procedure trigger_add_recent_track();
