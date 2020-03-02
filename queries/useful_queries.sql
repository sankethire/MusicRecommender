-- list all table rows --
select table_name, pg_relation_size(quote_ident(table_name))
from information_schema.tables
where table_schema = 'public'
order by 2;

select pg_size_pretty( pg_total_relation_size('table_name'));
