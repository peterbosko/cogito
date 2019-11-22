SHOW FULL COLUMNS FROM sl;

delete from sl where id in (
select id from sl s where pad='Vok' and exists (select 1 from sl s2 WHERE s.sd_id=s2.sd_id AND s.tvar=s2.tvar)
)



/*delete from sl where pad='Vok' and id>0*/