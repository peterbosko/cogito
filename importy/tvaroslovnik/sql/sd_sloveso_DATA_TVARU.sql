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
REPLACE(t1.data_tvaru,
'zvratnosť: sa;',''),
'zvratnosť: si;',''),
'negácia: ne-;',''),
'forma: prechodník;',''),
'číslo: jednotné;',''),
'číslo: množné;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'forma: neurčitok;',''),
'osoba: prvá;',''),
'osoba: druhá;',''),
'osoba: tretia;',''),
'čas: prítomný;',''),
'čas: minulý;',''),
'čas: budúci;',''),
'spôsob: rozkazovací;',''),
'spôsob: oznamovací;','')
rep,
t1.*,t2.tvar
from tvary.tvary t1 join tvary.tvary t2 on t1.id_zakladneho_tvaru=t2.id
where t1.data_zakladneho_tvaru like 'sloveso%' and t1.data_tvaru not like '%príčastie%' and t1.data_tvaru not like '%podstatné%'
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
REPLACE(t1.data_tvaru,
'zvratnosť: sa;',''),
'zvratnosť: si;',''),
'negácia: ne-;',''),
'forma: prechodník;',''),
'číslo: jednotné;',''),
'číslo: množné;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'rod: stredný;',''),
'forma: neurčitok;',''),
'osoba: prvá;',''),
'osoba: druhá;',''),
'osoba: tretia;',''),
'čas: prítomný;',''),
'čas: minulý;',''),
'čas: budúci;',''),
'spôsob: rozkazovací;',''),
'spôsob: oznamovací;','')
!=''

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
REPLACE(data_tvaru,
'negácia: ne-;',''),
'forma: slovesné podstatné meno;',''),
'zvratnosť: sa;',''),
'zvratnosť: si;',''),
'číslo: jednotné;',''),
'číslo: množné;',''),
'pád: nominatív;',''),
'pád: genitív;',''),
'pád: datív;',''),
'pád: akuzatív;',''),
'pád: vokatív;',''),
'pád: lokál;',''),
'pád: inštrumentál;','')
rep,
t.* 
from tvary.tvary t
where data_tvaru like '%slovesné pods%' 
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
REPLACE(data_tvaru,
'negácia: ne-;',''),
'forma: slovesné podstatné meno;',''),
'zvratnosť: sa;',''),
'zvratnosť: si;',''),
'číslo: jednotné;',''),
'číslo: množné;',''),
'pád: nominatív;',''),
'pád: genitív;',''),
'pád: datív;',''),
'pád: akuzatív;',''),
'pád: vokatív;',''),
'pád: lokál;',''),
'pád: inštrumentál;','')
!=''



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
REPLACE(
REPLACE(data_tvaru,
'podrod: životné;',''),
'podrod: neživotné;',''),
'rod: žitský;',''),
'rod: stredný;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'forma: činné príčastie;',''),
'forma: trpné príčastie;',''),
'forma: minulé príčastie;',''),
'negácia: ne-;',''),
'forma: slovesné podstatné meno;',''),
'zvratnosť: sa;',''),
'zvratnosť: si;',''),
'číslo: jednotné;',''),
'číslo: množné;',''),
'pád: nominatív;',''),
'pád: genitív;',''),
'pád: datív;',''),
'pád: akuzatív;',''),
'pád: vokatív;',''),
'pád: lokál;',''),
'pád: inštrumentál;','') 
rep,
t.* 
from tvary.tvary t
where data_tvaru like '%príčastie%' 
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
REPLACE(
REPLACE(data_tvaru,
'podrod: životné;',''),
'podrod: neživotné;',''),
'rod: žitský;',''),
'rod: stredný;',''),
'rod: mužský;',''),
'rod: ženský;',''),
'forma: činné príčastie;',''),
'forma: trpné príčastie;',''),
'forma: minulé príčastie;',''),
'negácia: ne-;',''),
'forma: slovesné podstatné meno;',''),
'zvratnosť: sa;',''),
'zvratnosť: si;',''),
'číslo: jednotné;',''),
'číslo: množné;',''),
'pád: nominatív;',''),
'pád: genitív;',''),
'pád: datív;',''),
'pád: akuzatív;',''),
'pád: vokatív;',''),
'pád: lokál;',''),
'pád: inštrumentál;','') 
!=''


limit 10000000