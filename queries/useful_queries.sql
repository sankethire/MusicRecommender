-- list all table rows --
select table_name, pg_relation_size(quote_ident(table_name))
from information_schema.tables
where table_schema = 'public'
order by 2
