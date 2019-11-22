select 
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(t1.data_zakladneho_tvaru,'podstatné meno|',''),
'pád: nominatív;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'podrod: neživotné;',''),
'podrod: životný;',''),
' pomnožné;',''),
'číslo: ',''),
' jednotné;',''),
' množné;',''),
'pád:',''),
'podrod: neživotný;',''),
'podrod: životné;','')


rep,
t1.*,t2.tvar
from tvary t1 join tvary t2 on t1.id_zakladneho_tvaru=t2.id
where t1.data_zakladneho_tvaru like 'podstatné meno%'
and 
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(t1.data_zakladneho_tvaru,'podstatné meno|',''),
'pád: nominatív;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'podrod: neživotné;',''),
'podrod: životný;',''),
' pomnožné;',''),
'číslo: ',''),
' jednotné;',''),
' množné;',''),
'pád:',''),
'podrod: neživotný;',''),
'podrod: životné;','')

!=''
