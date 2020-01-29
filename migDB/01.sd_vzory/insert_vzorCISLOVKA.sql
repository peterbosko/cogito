select * from sd_vzor where typ='CISLOVKA'
delete from sd_vzor where id>205
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','Z','jeden','en,ného,nému,ného,nom,ným,ni,ných,ným,ných,ných,nými',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','N','jeden','en,ného,nému,ného,nom,ným,ny,ných,ným,ných,ných,nými',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'jeden','na,nej,nej,nu,nej,ným,ny,ných,ným,ný,ných,nými',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','S',null,'jeden','no,ného,nému,no,nom,ným,ny,ných,ným,ny,ných,nými',null,'sklon','');

update sd_vzor 
set popis='Základná číslovka - končiaca na jeden'
where vzor='jeden'

update sd_vzor 
set popis='Základná číslovka - končiaca na aja - dvaja, traja'
where vzor='dva'

insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','Z','dva','x,x,x,x,x,x,aja,och,om,och,och,omi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','N','dva','x,x,x,x,x,x,a,och,om,a,och,omi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'dva','x,x,x,x,x,x,e,och,om,e,och,omi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','S',null,'dva','x,x,x,x,x,x,e,och,om,e,och,omi',null,'sklon','');

update sd_vzor 
set popis='Základná číslovka - končiaca na ia - štyria'
where vzor='štyri'


insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','Z','štyri','x,x,x,x,x,x,ia,och,om,och,och,mi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','N','štyri','x,x,x,x,x,x,i,och,om,i,och,mi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'štyri','x,x,x,x,x,x,i,och,om,i,och,mi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','S',null,'štyri','x,x,x,x,x,x,i,och,om,i,och,mi',null,'sklon','');

update sd_vzor 
set popis='Základná číslovka - končiaca na ať - desať, dvadsať'
where vzor='desať'



insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','Z','desať','x,x,x,x,x,x,iati,iatich,iatim,iatich,iatich,iatimi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','N','desať','x,x,x,x,x,x,ať,iatich,iatim,ať,iatich,iatimi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'desať','x,x,x,x,x,x,ať,iatich,iatim,ať,iatich,iatimi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','S',null,'desať','x,x,x,x,x,x,ať,iatich,iatim,ať,iatich,iatimi',null,'sklon','');

select * from sd_vzor where vzor='ulica'
update sd_vzor 
set popis='Radová číslovka - končiaca na ý - prvý, druhý, štvrtý'
where vzor='prvý'


insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','Z','prvý','ý,ého,ému,ého,om,ým,í,ých,ým,ých,ých,ými',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','N','prvý','ý,ého,ému,ého,om,ým,é,ých,ým,é,ých,ými',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'prvý','á,ej,ej,ú,ej,ou,é,ých,ým,é,ých,ými',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','S',null,'prvý','é,ého,ému,é,om,ým,é,ých,ým,é,ých,ými',null,'sklon','');

update sd_vzor 
set popis='Radová číslovka - končiaca na í - tretí'
where vzor='tretí'

insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','Z','tretí','í,ieho,iemu,ieho,om,ími,ie,ích,ím,ie,ích,ími',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','N','tretí','í,ieho,iemu,ieho,om,ími,ie,ích,ím,ie,ích,ími',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'tretí','ia,ej,ej,iu,ej,ou,ie,ích,ím,ie,ích,ími',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','S',null,'tretí','ie,ieho,iemu,ie,om,ím,ie,ích,ím,ie,ích,ími',null,'sklon','');

update sd_vzor 
set popis='Radová číslovka - končiaca na y - piaty, šiesty'
where vzor='piaty'

insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','Z','piaty','y,eho,emu,eho,om,ym,i,ych,ym,ych,ych,ymi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','M','N','piaty','y,eho,emu,eho,om,ym,e,ych,ym,e,ych,ymi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'piaty','a,ej,ej,u,ej,ou,e,ych,ym,e,ych,ymi',null,'sklon','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','S',null,'piaty','e,eho,emu,e,om,ym,e,ych,ym,e,ych,ym',null,'sklon','');

update sd_vzor 
set popis='Zlomková číslovka - končiaca na na - tretina, štvrtina'
where vzor='tretina'

insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'tretina','a,y,e,u,e,ou,y,,ám,y,ách,ami',null,'sklon','');
update sd_vzor 
set popis='Zlomková číslovka - končiaca na ca - polovica, štvorica'
where vzor='polovica'
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('CISLOVKA','Z',null,'polovica','a,e,i,u,i,ou,e,,iam,e,iach,ami',null,'sklon','');

insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('PRISLOVKA','',null,'belaso','',null,'stup','');
insert into sd_vzor(typ,rod,podrod,vzor,deklinacia,alternacia,sklon_stup,popis)
values('PRISLOVKA','',null,'samovzor','',null,'stup','');



select sd.zak_tvar, count(1) 
from sd join sd_cislovka on sd.id = sd_cislovka.id
group by sd.zak_tvar
having count(1)>1

update sd_vzor
set vzor='samovzor'
where id=161

select * from 

update sd
set vzor_stup='samovzor' 
where vzor_stup='suplet'
join sd_cislovka on sd.id=sd_cislovka.id

select sd.zak_tvar, sl.* from sl 
join sd on sl.sd_id=sd.id and sd.typ='CISLOVKA'
limit 0,1000000
where 

select * from sl where tvar='polovica'

select * from sl where sd_id in (100589,498512)