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
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(t1.data_zakladneho_tvaru,'prídavné meno|',''),
'prídavné meno privlastňovacie|',''),
'pád: nominatív;',''),
'pád: inštrumentál;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'podrod: neživotné;',''),
'podrod: životný;',''),
' pomnožné;',''),
'číslo: ',''),
' jednotné;',''),
' množné;',''),
'stupeň: prvý;',''),
'stupeň: druhý;',''),
'stupeň: tretí;',''),
'podrod: neživotný;',''),
'podrod: životné;','')

rep,
t1.*,t2.tvar
from tvary.tvary t1 join tvary.tvary t2 on t1.id_zakladneho_tvaru=t2.id
where t1.data_zakladneho_tvaru like 'prídavné meno%'
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
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(t1.data_zakladneho_tvaru,'prídavné meno|',''),
'prídavné meno privlastňovacie|',''),
'pád: nominatív;',''),
'pád: inštrumentál;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'podrod: neživotné;',''),
'podrod: životný;',''),
' pomnožné;',''),
'číslo: ',''),
' jednotné;',''),
' množné;',''),
'stupeň: prvý;',''),
'stupeň: druhý;',''),
'stupeň: tretí;',''),
'podrod: neživotný;',''),
'podrod: životné;','')
!=''
