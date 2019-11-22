select 

t2.tvar,t1.*
from tvary t1 join tvary t2 on t1.id_zakladneho_tvaru=t2.id
where t1.data_zakladneho_tvaru like 'spojka%'

