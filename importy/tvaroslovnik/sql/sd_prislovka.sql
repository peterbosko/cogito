select 
REPLACE(
REPLACE(
REPLACE(t1.data_zakladneho_tvaru,'príslovka',''),
'|stupeň: prvý;',''),
' ','')
rep,
t2.tvar,t1.*
from tvary.tvary t1 join tvary.tvary t2 on t1.id_zakladneho_tvaru=t2.id
where t1.data_zakladneho_tvaru like 'príslovka%'
and 
REPLACE(
REPLACE(
REPLACE(t1.data_zakladneho_tvaru,'príslovka',''),
'|stupeň: prvý;',''),
' ','')
!=''
select * from tvary.tvary t where t.data_zakladneho_tvaru like '%príslovka%'