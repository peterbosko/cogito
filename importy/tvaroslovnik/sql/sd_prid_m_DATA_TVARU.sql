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
REPLACE(
REPLACE(
REPLACE(
REPLACE(t1.data_tvaru,
'pád: nominatív;',''),
'pád: genitív;',''),
'pád: datív;',''),
'pád: akuzatív;',''),
'pád: vokatív;',''),
'pád: lokál;',''),
'pád: inštrumentál;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'podrod: neživotný;',''),
'podrod: životný;',''),
'podrod: neživotné;',''),
'podrod: životné;',''),
'stupeň: prvý;',''),
'stupeň: druhý;',''),
'stupeň: tretí;',''),
'číslo: ',''),
' jednotné;',''),
' množné;',''),
' pomnožné;','')
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
REPLACE(
REPLACE(
REPLACE(
REPLACE(t1.data_tvaru,
'pád: nominatív;',''),
'pád: genitív;',''),
'pád: datív;',''),
'pád: akuzatív;',''),
'pád: vokatív;',''),
'pád: lokál;',''),
'pád: inštrumentál;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'podrod: neživotný;',''),
'podrod: životný;',''),
'podrod: neživotné;',''),
'podrod: životné;',''),
'stupeň: prvý;',''),
'stupeň: druhý;',''),
'stupeň: tretí;',''),
'číslo: ',''),
' jednotné;',''),
' množné;',''),
' pomnožné;','')
!=''
