from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session
from app.c_models import *
from app.sd_models import *
from sqlalchemy.orm import aliased
import sqlalchemy as sa
from sqlalchemy_utils import (
    create_view,
)


db = SQLAlchemy()


class Log(db.Model):
    __tablename__ = 'l'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    IP = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(2000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("u.id"), nullable=True)
    cas = db.Column(db.DateTime(), nullable=False)
    user_agent = db.Column(db.String(100), nullable=True)


class User(db.Model):
    __tablename__ = 'u'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    meno = db.Column(db.String(255), nullable=False)
    priezvisko = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.String(2), nullable=False)
    je_admin = db.Column(db.String(1), nullable=True)
    je_metadata_admin = db.Column(db.String(1), nullable=True)
    je_admin_slov = db.Column(db.String(1), nullable=True)

    def nastav_heslo(self, password):
        self.password = generate_password_hash(password)

    def skontroluj_heslo(self, password):
        return check_password_hash(self.password, password)


class Kontext(db.Model):
    __tablename__ = 'kt'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    nazov = db.Column(db.String(255), nullable=False)
    obsah = db.Column(db.Text(4000000000), nullable=False)
    text = db.Column(db.Text(4000000000))
    status = db.Column(db.String(2), nullable=False)
    zoznam_slov = db.Column(db.Text, nullable=True)
    autor_id = db.Column(db.Integer, db.ForeignKey("u.id"), nullable=False)
    autor = relationship("User")

    def mam_prava(self):
        if "logged" in session.keys():
            usr = int(session["logged"])
            ja = User.query.get(usr)
            if usr == self.autor_id or ja.je_admin == "A":
                return True
            else:
                return False
        else:
            return False


class SlovnyDruh(db.Model):
    __tablename__ = 'sd'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    zak_tvar = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False)
    typ = db.Column(db.String(20), nullable=False, index=True)
    popis = db.Column(db.String(2000), nullable=True)
    slova = relationship("Slovo", back_populates="SlovnyDruh")
    vzor = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=True)
    prefix = db.Column(db.String(20, collation='utf8mb4_bin'), nullable=True)
    sufix = db.Column(db.String(20, collation='utf8mb4_bin'), nullable=True)
    sem_priznak_id = db.Column(db.Integer, db.ForeignKey("sem.id"), nullable=True, index=True)
    sem_priznak = relationship("Semantika", foreign_keys=[sem_priznak_id])
    sd_hier = relationship("HierarchiaSD", primaryjoin="(SlovnyDruh.id==HierarchiaSD.sd_id)")

    __mapper_args__ = {
        'polymorphic_identity': 'sd',
        'polymorphic_on': typ
    }

    def exportuj(self):
        export = SlovnyDruhExport()
        export.id = self.id
        export.zak_tvar = self.zak_tvar
        export.typ = self.typ
        export.parent_sd_id = self.parent_sd_id
        return export

    def exportujSem(self):
        export = SlovnyDruhExport()
        export.id = self.id
        export.zak_tvar = self.zak_tvar
        export.typ = self.typ
        if self.sem_priznak.id:
            odvodene = SemHierarchia.query.filter(SemHierarchia.sem_id == sem_priznak.id)
        
        return export

    def exportujPlnySD(self):
        export = SDExport()
        export.zak_tvar = self.zak_tvar
        export.popis = self.popis
        export.typ = self.typ

        if self.typ == "POD_M":
            pm = PodstatneMeno.query.get(self.id)
            export.rod = pm.rod
            export.podrod = pm.podrod
            export.sloveso_id = pm.sloveso_id
            
            if pm.sloveso_id:
                slov = Sloveso.query.get(pm.sloveso_id)

                export.sloveso_tvar = slov.zak_tvar

                if slov.zvratnost:
                    export.sloveso_tvar += " " + slov.zvratnost

        elif self.typ == "PRID_M":
            prm = PridavneMeno.query.get(self.id)
            export.sloveso_id = prm.sloveso_id

            if prm.sloveso_id:
                slov = Sloveso.query.get(prm.sloveso_id)

                export.sloveso_tvar = slov.zak_tvar

                if slov.zvratnost:
                    export.sloveso_tvar += " " + slov.zvratnost

            export.je_privlastnovacie = prm.je_privlastnovacie
        elif self.typ == "ZAMENO":
            zam = Zameno.query.get(self.id)
            export.rod = zam.rod
            export.podrod = zam.podrod
            export.cislo = zam.cislo
        elif self.typ == "SLOVESO":
            s = Sloveso.query.get(self.id)
            export.zvratnost = s.zvratnost
            export.je_negacia = s.je_negacia
            export.sloveso_id = s.pozitivne_sloveso_id

            if s.pozitivne_sloveso_id:
                slov = Sloveso.query.get(s.pozitivne_sloveso_id)
                export.sloveso_tvar = slov.zak_tvar

                if slov.zvratnost:
                    export.sloveso_tvar += " " + slov.zvratnost

        elif self.typ == "PREDLOZKA":
            pr = Predlozka.query.get(self.id)
            export.pady = pr.pady
        elif self.typ == "CISLOVKA":
            cis = Cislovka.query.get(self.id)
            export.rod = cis.rod
            export.podrod = cis.podrod
            export.cislo = cis.cislo
            export.hodnota = cis.hodnota

        export.slova = Slovo.query.filter(Slovo.sd_id == self.id).all()

        return export


class Sloveso(SlovnyDruh):
    __tablename__ = 'sd_sloveso'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    sd_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    je_negacia = db.Column(db.String(1), nullable=True)
    pozitivne_sloveso_id = db.Column('pozitivne_sloveso_id', db.Integer, db.ForeignKey('sd_sloveso.id'), nullable=True)
    zvratnost = db.Column(db.String(20), nullable=True)
    vid = db.Column(db.String(10), nullable=True)
    int_ramec_id = db.Column(db.Integer, db.ForeignKey("int_ramec.id"), nullable=True, index=True)
    int_ramec = relationship("IntencnyRamec", foreign_keys=[int_ramec_id])
    pzkmen = db.Column(db.String(20), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'SLOVESO',
    }


class PodstatneMeno(SlovnyDruh):
    __tablename__ = 'sd_pod_m'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    pod_m_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    rod = db.Column(db.String(1), nullable=False)
    podrod = db.Column(db.String(1), nullable=True)
    sloveso_id = db.Column(db.Integer, db.ForeignKey("sd_sloveso.id"), nullable=True, index=True)
    sloveso = relationship("Sloveso", foreign_keys=[sloveso_id])
    je_negacia = db.Column(db.String(1), nullable=True)
    pocitatelnost = db.Column(db.String(20), nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'POD_M',
    }


class PridavneMeno(SlovnyDruh):
    __tablename__ = 'sd_prid_m'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    prid_m_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    sloveso_id = db.Column(db.Integer, db.ForeignKey("sd_sloveso.id"), nullable=True, index=True)
    sloveso = relationship("Sloveso", foreign_keys=[sloveso_id])
    je_privlastnovacie = db.Column(db.String(1), nullable=False)
    je_negacia = db.Column(db.String(1), nullable=True)
    sem_priznak_prid_m_id = db.Column(db.Integer, db.ForeignKey("sem.id"), nullable=True, index=True)
    sem_priznak_prid_m = relationship("Semantika", foreign_keys=[sem_priznak_prid_m_id])
    vzor2 = db.Column(db.String(50), nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'PRID_M',
    }
    def exportuj(self):
        export = self

        return export

class Zameno(SlovnyDruh):
    __tablename__ = 'sd_zameno'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    zameno_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    cislo = db.Column(db.String(1), nullable=True)
    rod = db.Column(db.String(1), nullable=True)
    podrod = db.Column(db.String(1), nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'ZAMENO',
    }


class Prislovka(SlovnyDruh):
    __tablename__ = 'sd_prislovka'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    prislovka_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    sem_pad_id = db.Column('sem_pad', db.Integer, db.ForeignKey('sem_pad.id'))
    koncovka = db.Column(db.String(50), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'PRISLOVKA',
    }


class Cislovka(SlovnyDruh):
    __tablename__ = 'sd_cislovka'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    cislovka_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    hodnota = db.Column(db.String(50), nullable=True)
    rod = db.Column(db.String(1), nullable=True)
    podrod = db.Column(db.String(1), nullable=True)
    cislo = db.Column(db.String(1), nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'CISLOVKA',
    }


class Predlozka(SlovnyDruh):
    __tablename__ = 'sd_predlozka'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    predlozka_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    pady = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'PREDLOZKA',
    }


class Citoslovce(SlovnyDruh):
    __tablename__ = 'sd_citoslovce'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    __mapper_args__ = {
        'polymorphic_identity': 'CITOSLOVCE',
    }
    citoslovce_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)


class Spojka(SlovnyDruh):
    __tablename__ = 'sd_spojka'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    __mapper_args__ = {
        'polymorphic_identity': 'SPOJKA',
    }
    spojka_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)


class Castica(SlovnyDruh):
    __tablename__ = 'sd_castica'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    __mapper_args__ = {
        'polymorphic_identity': 'CASTICA',
    }
    castica_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)


class Ostatne(SlovnyDruh):
    __tablename__ = 'sd_ostatne'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    __mapper_args__ = {
        'polymorphic_identity': 'OSTATNE',
    }
    ostatne_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)


class Slovo(db.Model):
    __tablename__ = 'sl'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    tvar = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False, index=True)
    rod = db.Column(db.String(1), nullable=True)
    podrod = db.Column(db.String(1), nullable=True)
    pad = db.Column(db.String(3), nullable=True)
    stupen = db.Column(db.String(1), nullable=True)
    sposob = db.Column(db.String(1), nullable=True)
    osoba = db.Column(db.String(1), nullable=True)
    cas = db.Column(db.String(1), nullable=True)
    pricastie = db.Column(db.String(1), nullable=True)
    cislo = db.Column(db.String(1), nullable=True)
    je_negacia = db.Column(db.String(1), nullable=True)
    je_neurcitok = db.Column(db.String(1), nullable=True)
    je_prechodnik = db.Column(db.String(1), nullable=True)
    zvratnost = db.Column(db.String(20), nullable=True)
    anotacia = db.Column(db.String(10), nullable=True)
    sd_id = db.Column('sd_id', db.Integer, db.ForeignKey('sd.id'))
    zmenene = db.Column(db.DateTime(), nullable=True)
    SlovnyDruh = relationship("SlovnyDruh", foreign_keys=[sd_id], back_populates="slova")
    user_id = db.Column(db.Integer, db.ForeignKey("u.id"), nullable=True)

    def exportuj(self, prvy_znak_upper):
        export = SlovoExport()
        export.id = self.id
        export.tvar = self.tvar
        export.zak_tvar = self.SlovnyDruh.zak_tvar
        export.popis = self.SlovnyDruh.popis
        if prvy_znak_upper:
            export.tvar = export.tvar[0].upper() + export.tvar[1:]
        export.rod = self.rod
        export.podrod = self.podrod
        export.pad = self.pad
        export.stupen = self.stupen
        export.sposob = self.sposob
        export.osoba = self.osoba
        export.cas = self.cas
        export.pricastie = self.pricastie
        export.cislo = self.cislo
        export.je_negacia = self.je_negacia
        export.je_neurcitok = self.je_neurcitok
        export.je_prechodnik = self.je_prechodnik
        export.zvratnost = self.zvratnost
        export.sd_id = self.sd_id
        export.slovny_druh = self.SlovnyDruh.typ
        export.anotacia = self.anotacia
        export.sem_id = self.SlovnyDruh.sem_priznak_id
        export.sufix = self.SlovnyDruh.sufix
        export.prefix = self.SlovnyDruh.prefix
        export.vzor = self.SlovnyDruh.vzor

        if export.slovny_druh == "PREDLOZKA":
            predlozka = Predlozka.query.get(export.sd_id)
            export.zoznam_padov = predlozka.pady

        return export
        
        
class UnitTest(db.Model):
    __tablename__ = 'kt_ut'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    kontext_id = db.Column('kt_id', db.Integer, db.ForeignKey('kt.id'))
    kontext = relationship("Kontext", uselist=False)
    poradie = db.Column(db.Integer, nullable=False)
    funkcia = db.Column(db.String(255), nullable=False)
    nazov = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(1), nullable=False)
    datum_posledneho_behu = db.Column(db.DateTime(), nullable=True)
    spustac_posledneho_behu = db.Column(db.Integer, db.ForeignKey("u.id"), nullable=True)
    zadanie = db.Column(db.Text, nullable=True)
    ocakavany_vysledok = db.Column(db.Text, nullable=True)
    skutocny_vysledok = db.Column(db.Text, nullable=True)
    rozdiel = db.Column(db.Text, nullable=True)
    autor_id = db.Column(db.Integer, db.ForeignKey("u.id"), nullable=False)

    def exportuj(self):
        export = UnitTestExport()
        export.id = self.id
        export.kontext_id = self.kontext_id
        export.status = self.status
        export.funkcia = self.funkcia
        export.poradie = self.poradie

        return export

    def mam_prava(self):
        if "logged" in session.keys():
            usr = int(session["logged"])
            ja = User.query.get(usr)
            if usr == self.autor_id or ja.je_admin == "A":
                return True
            else:
                return False
        else:
            return False


class SemantickyPad(db.Model):
    __tablename__ = 'sem_pad'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    kod = db.Column(db.String(20, collation='utf8mb4_bin'), nullable=False)
    nazov = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False)


class Semantika(db.Model):
    __tablename__ = 'sem'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    kod = db.Column(db.String(20, collation='utf8mb4_bin'), nullable=False)
    nazov = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False)


class SemHierarchia(db.Model):
    __tablename__ = 'sem_hier'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    sem_id = db.Column('sem_id', db.Integer, db.ForeignKey('sem.id'))
    sem = relationship("Semantika", foreign_keys=[sem_id])
    rodic_id = db.Column('rodic_id', db.Integer, db.ForeignKey('sem.id'), nullable=True)
    rodic = relationship("Semantika", foreign_keys=[rodic_id])


class IntencnyRamec(db.Model):
    __tablename__ = 'int_ramec'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    kod = db.Column(db.String(20), nullable=True)
    nazov = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False)


class Intencia(db.Model):
    __tablename__ = 'int'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    int_ramec_id = db.Column('int_ramec_id', db.Integer, db.ForeignKey('int_ramec.id'))
    int_ramec = relationship("IntencnyRamec", uselist=False, lazy='joined')
    predlozka = db.Column(db.String(50), nullable=True)
    pad = db.Column(db.String(3), nullable=True)
    sem_priznak_id = db.Column('sem', db.Integer, db.ForeignKey('sem.id'))
    sem_pad = relationship("SemantickyPad", uselist=False, lazy='joined')
    sem_priznak = relationship("Semantika", uselist=False, lazy='joined')
    sem_pad_id = db.Column('sem_pad', db.Integer, db.ForeignKey('sem_pad.id'))
    fl = db.Column('fl', db.Integer, nullable=True)


class HierarchiaSD(db.Model):
    __tablename__ = 'sd_hier'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    sd_id = db.Column('sd_id', db.Integer, db.ForeignKey('sd.id'), nullable=False)
    sd = relationship("SlovnyDruh", foreign_keys=[sd_id])
    parent_sd_id = db.Column('parent_sd_id', db.Integer, db.ForeignKey('sd.id'), nullable=False)
    parent_sd = relationship("SlovnyDruh", foreign_keys=[parent_sd_id])

    def exportuj(self):
        export = SlovnyDruhHierExport()
        export.id = self.id
        export.sd_id = self.sd_id
        export.parent_sd_id = self.parent_sd_id
        export.sd = self.sd
        export.parent_sd = self.parent_sd

        return export

sem1 = aliased(Semantika, name='sem1')
sem2 = aliased(Semantika, name='sem2')
sd = aliased(SlovnyDruh, name='sd')
pm = aliased(PridavneMeno, name='pm')


class SemHierarchiaView(db.Model):
    __table__ = create_view(
        name='sem_hier_v',
        selectable=sa.select(
            [
                SemHierarchia.id,
                sem1.id.label('sem_priznak_id'),
                sem1.typ,
                sem1.kod,
                sem1.nazov,
                SemHierarchia.rodic_id,
                sem2.kod.label('rodic_kod'),
                sem2.nazov.label('rodic_nazov'),
                sa.select([sa.func.count()], from_obj=sd).where(sd.sem_priznak_id == SemHierarchia.sem_id)
                    .label('pocet_slov'),
                sa.select([sa.func.count()], from_obj=pm).where(pm.sem_priznak_prid_m_id == SemHierarchia.sem_id)
                    .label('pocet_slov_prid_m'),
            ],
            from_obj=(
                SemHierarchia.__table__.join(sem1, sem1.id == SemHierarchia.sem_id)
                .outerjoin(sem2, sem2.id == SemHierarchia.rodic_id)
            )
        ),
        metadata=db.Model.metadata
    )


class IntencnyRamecView(db.Model):
    __table__ = create_view(
        name='int_ramec_v',
        selectable=sa.select(
            [
                IntencnyRamec.id,
                IntencnyRamec.kod,
                IntencnyRamec.nazov,
                sa.select([sa.func.count()], from_obj=Intencia).where(Intencia.int_ramec_id == IntencnyRamec.id)
                    .label('pocet_intencii'),
                sa.select([sa.func.count()], from_obj=Sloveso).where(Sloveso.int_ramec_id == IntencnyRamec.id)
                    .label('pocet_slovies'),
            ],
            from_obj=(
                IntencnyRamec.__table__
            )
        ),
        metadata=db.Model.metadata
    )


class SemantickyPadView(db.Model):
    __table__ = create_view(
        name='sem_pad_v',
        selectable=sa.select(
            [
                SemantickyPad.id,
                SemantickyPad.kod,
                SemantickyPad.nazov,
                sa.select([sa.func.count()], from_obj=Intencia).where(Intencia.sem_pad_id == SemantickyPad.id)
                    .label('pocet_intencii'),
                sa.select([sa.func.count(sa.distinct(Sloveso.sd_id))], from_obj=Sloveso.__table__.
                          join(Intencia, Intencia.int_ramec_id == Sloveso.int_ramec_id)).
                    where(Intencia.sem_pad_id == SemantickyPad.id).label('pocet_slovies'),
            ],
            from_obj=SemantickyPad.__table__
        ),
        metadata=db.Model.metadata
    )


class SlovesoView(db.Model):
    __table__ = create_view(
        name='sd_sloveso_v',
        selectable=sa.select(
            [
                Sloveso.sd_id.label('id'),
                SlovnyDruh.zak_tvar,
                Sloveso.popis,
                Sloveso.zvratnost,
                Sloveso.vid,
                Sloveso.int_ramec_id,
                sa.select([IntencnyRamec.kod], from_obj=IntencnyRamec).where(IntencnyRamec.id == Sloveso.int_ramec_id)
                    .label('int_ramec_kod'),
                sa.select([IntencnyRamec.nazov], from_obj=IntencnyRamec).where(IntencnyRamec.id == Sloveso.int_ramec_id)
                    .label('int_ramec_nazov'),
                Sloveso.je_negacia,
                Sloveso.pozitivne_sloveso_id,
            ],
            from_obj=Sloveso.__table__.join(SlovnyDruh, SlovnyDruh.id == Sloveso.sd_id)
        ),
        metadata=db.Model.metadata
    )


class IntencieSlovesaView(db.Model):
    __table__ = create_view(
        name='int_slovesa_v',
        selectable=sa.select(
            [
                Intencia.id.label('id'),
                # sa.func.row_number().over(order_by=[Sloveso.sd_id]).label('id'),
                # Sloveso.sd_id.label('id'),
                Sloveso.sd_id.label('sd_id'),
                SlovnyDruh.zak_tvar.label('zak_tvar'),
                Sloveso.zvratnost,
                Sloveso.popis,
                Sloveso.vid,
                Sloveso.int_ramec_id,
                Intencia.typ,
                Intencia.predlozka,
                Intencia.pad,
                Intencia.sem_priznak_id.label('sem_priznak_id'),
                sa.select([Semantika.kod], from_obj=Semantika).where(Semantika.id == Intencia.sem_priznak_id)
                    .label('sem_kod'),
                Intencia.sem_pad_id.label('sem_pad_id'),
                sa.select([SemantickyPad.nazov], from_obj=SemantickyPad).where(SemantickyPad.id == Intencia.sem_pad_id)
                    .label('sp_nazov'),
                sa.select([IntencnyRamec.kod], from_obj=IntencnyRamec).where(Intencia.int_ramec_id == IntencnyRamec.id)
                    .label('ir_kod'),
                sa.select([IntencnyRamec.nazov], from_obj=IntencnyRamec).where(Intencia.int_ramec_id == IntencnyRamec.id)
                    .label('ir_nazov'),
                Intencia.fl.label('fl'),
            ],
            from_obj=Sloveso.__table__.join(SlovnyDruh, SlovnyDruh.id == Sloveso.sd_id).
                join(Intencia, Intencia.int_ramec_id == Sloveso.int_ramec_id)
        ),
        metadata=db.Model.metadata
    )

