select 
REPLACE(
REPLACE(
REPLACE(t1.data_tvaru,
'stupeň: prvý;',''),
'stupeň: druhý;',''),
'stupeň: tretí;','')
rep,
t1.*,t2.tvar
from tvary.tvary t1 join tvary.tvary t2 on t1.id_zakladneho_tvaru=t2.id
where t1.data_zakladneho_tvaru like 'príslovka%'
and 
REPLACE(
REPLACE(
REPLACE(t1.data_tvaru,
'stupeň: prvý;',''),
'stupeň: druhý;',''),
'stupeň: tretí;','')
!=''


select tvar,data_zakladneho_tvaru,data_tvaru,t.id_zakladneho_tvaru,t.* from tvary.tvary t
where data_zakladneho_tvaru like 'príslovka%'