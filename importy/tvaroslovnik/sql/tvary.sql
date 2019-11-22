use tvary
SHOW TABLE STATUS like 'tvary'
ALTER TABLE tvary
column tvar
CHARACTER SET 'utf8'
COLLATE 'utf8_slovak_cs'

alter table cogito.kt CHARACTER SET=utf8mb4
ALTER TABLE tvary
CHARACTER SET utf8mb4
COLLATE 'utf8mb4_bin'


tvar
CHARACTER SET character_set_name
COLLATE collation_name
select * from tvary.tvary where tvar='á' COLLATE utf8_bin and id<100 
collation='utf8mb4_bin' 