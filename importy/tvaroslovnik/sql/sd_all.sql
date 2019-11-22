
﻿select *
from tvary t1 
inner join tvary t2 on t1.id_zakladneho_tvaru=t2.id 
where 

t1.data_zakladneho_tvaru not like 'podstatné meno%'
and t1.data_zakladneho_tvaru not like 'prídavné meno%'
and t1.data_zakladneho_tvaru not like 'sloveso%'
and t1.data_zakladneho_tvaru not like 'príslovka%'
and t1.data_zakladneho_tvaru not like 'číslovka%'
and t1.data_zakladneho_tvaru not like 'častica%'
and t1.data_zakladneho_tvaru not like 'spojka%'
and t1.data_zakladneho_tvaru not like 'zámeno%'
and t1.data_zakladneho_tvaru not like 'citoslovce%'
and t1.data_zakladneho_tvaru not like 'predložka%'
and t1.data_zakladneho_tvaru not like 'ustálené slovné spojenie'
and t1.data_zakladneho_tvaru not like 'značka'
and t1.data_zakladneho_tvaru not like 'skratka'
and t1.data_zakladneho_tvaru not like 'predpona'
and t1.data_zakladneho_tvaru not like 'prípona'
and t1.data_zakladneho_tvaru not like 'príslovkový výraz'
and t1.data_zakladneho_tvaru not like 'predložkový výraz'
and t1.data_zakladneho_tvaru not like 'spojkový výraz'


