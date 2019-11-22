select 
t2.tvar,t1.*
from tvary.tvary t1 join tvary.tvary t2 on t1.id_zakladneho_tvaru=t2.id
where t1.data_zakladneho_tvaru like 'číslovka%'
and  t1.data_zakladneho_tvaru like '%inštru%'




t1.id_zakladneho_tvaru=1506206
limit 10000000

