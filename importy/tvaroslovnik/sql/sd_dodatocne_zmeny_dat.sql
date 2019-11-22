SHOW FULL COLUMNS FROM sl;

delete from sl where id in (
select id from sl s where pad='Vok' and exists (select 1 from sl s2 WHERE s.sd_id=s2.sd_id AND s.tvar=s2.tvar)
)

select * from sl join sd on sl.sd_id=sd.id where tvar='čo'
select * from sl join sd on sl.sd_id=sd.id where tvar='kto'

select * from sd_predlozka p
join sd on sd.id=p.id
where sd.id= 221374

select * from tvary.tvary where tvar='po'

SELECT t1.* ,p.id FROM `tvary`.`tvary` t1 
JOIN cogito.sl s ON t1.slovo_id=s.id
JOIN cogito.sd_predlozka p on p.id=s.sd_id
WHERE p.id=90683 
/*delete from sl where pad='Vok' and id>0*/