use cogito;
drop table sl;
drop table sd_cislovka;
drop table sd_prid_m;
drop table sd_pod_m;
drop table sd_zameno;
drop table sd_sloveso;
drop table sd_predlozka;
drop table sd_citoslovce;
drop table sd_spojka;
drop table sd_castica;
drop table sd_prislovka;
drop table sd;

update tvary.tvary set slovo_id = null
where id<=100000;
drop table kt;
drop table u;

SHOW FULL COLUMNS FROM tvary.tvary
SHOW FULL COLUMNS FROM sd
SHOW FULL COLUMNS FROM sl
SHOW FULL COLUMNS FROM kt

select * from sd join sd_prid_m on sd.id=sd_prid_m.id 
select * from sd join sd_sloveso on sd.id=sd_sloveso.id 
where sd.id=71

select * from sd_pod_m
select * from sd_prid_m where zvratnost is not null
select * from sd_sloveso
select * from sd join sd_prid_m p on sd.id=p.id
select * from sl where sd_id in (203,209,210) and tvar='absorbujúci'
select count(*) from sl 

limit 100000

where sd_id=3
show variables like '%collation%';
show table status like 'sd'
SHOW FULL COLUMNS FROM sd_pod_m 

alter table kt convert to character set utf8mb4 collate utf8mb4_bin;
alter table sd convert to character set utf8mb4 collate utf8mb4_bin;
alter table kt collation='utf8mb4_bin'

select * from sl join sd on sl.sd_id=sd.id
where tvar='a'

select * from tvary.tvary

select * from sd order by id desc

join sd_pod_m p on sd.id=p.id 

select t.tvar,t.data_zakladneho_tvaru,t.data_tvaru, count(1) from tvary.tvary t 
where t.slovo_id is not null
group by t.tvar,t.data_zakladneho_tvaru,t.data_tvaru 
having count(1)>1

select * from sd join sd_pod_m p on sd.id=p.id
where zak_tvar='mačka'
order by sd.id desc
limit 60000

select * from sd join sd_sloveso p on sd.id=p.id
where zak_tvar='liezť'
order by sd.id desc
limit 60000

select * from sd_predlozka p join sd on p.id=sd.id
sl where tvar='po'

select * from sd_prid_m
select * from sd_prislovka
select * from sd_sloveso
select * from sd_zameno

select * from sl where tvar='Peter'

sd_id=37416

where id=208
zak_tvar='alpínsky'

select * from sl where 
tvar='aktivovanej'


select * from tvary.tvary where tvar='Peter'

select * from sd_pod_m where id in (2182,2183)

select * from sl where sd_id in (2182,2183)

limit 2000000
where tvar 
like 'zvíťazil'
id_zakladneho_tvaru=14743644

t.data_zakladneho_tvaru like 'sloveso%'
tvar like 'behať'

select * from tvary.tvary t 
order by id 
where t.data_zakladneho_tvaru like 'sloveso%'
and t.data_tvaru like '%zvrat%'

select * from sl where tvar='a'
order by id desc

delete from sl where pad='Vok' and id>26917098

update tvary.tvary
set slovo_id=null
where id<=28


id_zakladneho_tvaru in (278413,279201)


limit 2000

where t.data_zakladneho_tvaru like '%sloveso%'

select * from tvary.tvary where tvar='po'

SELECT t1.*, t2.slovo_id parent_slovo_id FROM `tvary`.`tvary` t1 
LEFT OUTER JOIN tvary.tvary t2 ON t1.id_zakladneho_tvaru=t2.id
WHERE t1.`id`=15 AND ISNULL(t1.slovo_id)=1

select * from sl where tvar like 'po'
SELECT * FROM sd where id='90683'
select * from sd_predlozka where id=90683

is null order by id

select * from sl s where pad='Vok' and not exists (select 1 from sl s2 WHERE s.sd_id=s2.sd_id AND s.tvar=s2.tvar)


tvar like 'som'


select * from tvary.tvary where tvar='som' order by slovo_id desc

select * from tvary.tvary where slovo_id is null order by id limit 200000
tvar='som'

select max(t.id) from tvary.tvary t where slovo_id is null limit 2000000
select * from u

delete from u where id=9

delete from u where email='bosko.peter@gmail.com' and id>1


select * from kt


SELECT t1.*, sl.sd_id parent_sd_id FROM `tvary`.`tvary` t1 
LEFT OUTER JOIN tvary.tvary t2 ON t1.id_zakladneho_tvaru=t2.id 
LEFT OUTER JOIN cogito.sl ON sl.id=t2.slovo_id 
WHERE ISNULL(t1.slovo_id)=1
limit 10000
select count(*) from sd where zak_tvar like '% %'

select * from tvary.tvary where tvar='jeho'

select * from sd where id in (
select sd_id from cogito.sl where tvar='jeho'
)
delete from u where id=11
select * from u
select * from cogito.sl where tvar='jeho'
select * from cogito.sl where tvar like 'ten istý'
use cogito
select * from sl join sd on sl.sd_id=sd.id where tvar='po'
select * from tvary.tvary where (tvar='dobrá' and slovo_id=128751) OR id='1032349'
select * from sl join sd on sl.sd_id=sd.id where sd.id=190656
select * from sd_predlozka where id=90683


