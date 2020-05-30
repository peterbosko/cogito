from app.db.main import *
from app.db.koncept import *
from app.db.metadata import *


class SlovnyDruh(db.Model):
    __tablename__ = 'sd'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    zak_tvar = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False)
    typ = db.Column(db.String(20), nullable=False, index=True)
    koren = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False)
    popis = db.Column(db.String(2000), nullable=True)
    slova = relationship("Slovo", back_populates="SlovnyDruh")
    vzor = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=True, index=True)
    prefix = db.Column(db.String(20, collation='utf8mb4_bin'), nullable=True)
    sufix = db.Column(db.String(20, collation='utf8mb4_bin'), nullable=True)
    # sem_priznak_id = db.Column(db.Integer, db.ForeignKey("sem.id"), nullable=True, index=True)
    # sem_priznak = relationship("Semantika", foreign_keys=[sem_priznak_id])
    sem_priznaky = relationship("SlovnyDruhSemantika", back_populates="SlovnyDruh")
    paradigma = db.Column(db.String(1), nullable=True)
    vzor_stup = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(2), nullable=True)
    chyba = db.Column(db.String(2000), nullable=True)
    vzor_temp = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=True)
    zmenene = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("u.id"), nullable=True)
    koncept_id = db.Column(db.Integer, db.ForeignKey("kc.id"), nullable=True)
    # sd_hier = relationship("HierarchiaSD", primaryjoin="(SlovnyDruh.id==HierarchiaSD.sd_id)")

    __mapper_args__ = {
        'polymorphic_identity': 'sd',
        'polymorphic_on': typ
    }

    def daj_export_sem_priznaky(self):
        vysledok = ""
        for sem in self.sem_priznaky:
            if vysledok:
                vysledok += ";"
            vysledok += str(sem.sem_priznak_id)

        return vysledok

    def exportuj(self):
        export = SlovnyDruhExport()
        export.id = self.id
        export.zak_tvar = self.zak_tvar
        export.typ = self.typ
        return export

    def exportuj_zak_info(self):
        export = SlovnyDruhExport()
        export.zak_tvar = self.zak_tvar
        export.popis = self.popis
        export.typ = self.typ
        export.sem_priznaky = self.daj_export_sem_priznaky()
        export.vzor = self.vzor
        export.prefix = self.prefix
        export.sufix = self.sufix
        export.koren = self.koren
        export.vzor_stup = self.vzor_stup
        export.koncept_id = self.koncept_id
        if export.koncept_id:
            export.koncept_nazov = Koncept.query.get(export.koncept_id).nazov
        else:
            export.koncept_nazov = ""

        if self.typ == "POD_M":
            pm = PodstatneMeno.query.get(self.id)
            export.rod = pm.rod
            export.podrod = pm.podrod
            export.sloveso_id = pm.sloveso_id
            export.pocitatelnost = pm.pocitatelnost

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
        elif self.typ == "SLOVESO":
            s = Sloveso.query.get(self.id)
            export.zvratnost = s.zvratnost
            export.je_negacia = s.je_negacia
            export.sloveso_id = s.pozitivne_sloveso_id
            export.pzkmen = s.pzkmen
            export.vid = s.vid

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
            export.hodnota = cis.hodnota

        return export

    def exportuj_plny_sd(self):
        export = self.exportuj_zak_info()

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
    # sem_priznak_prid_m_id = db.Column(db.Integer, db.ForeignKey("sem.id"), nullable=True, index=True)
    # sem_priznak_prid_m = relationship("Semantika", foreign_keys=[sem_priznak_prid_m_id])
    __mapper_args__ = {
        'polymorphic_identity': 'PRID_M',
    }


class Zameno(SlovnyDruh):
    __tablename__ = 'sd_zameno'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    zameno_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'ZAMENO',
    }


class Prislovka(SlovnyDruh):
    __tablename__ = 'sd_prislovka'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    prislovka_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    koncovka = db.Column(db.String(50), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'PRISLOVKA',
    }


class Cislovka(SlovnyDruh):
    __tablename__ = 'sd_cislovka'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    cislovka_id = db.Column('id', db.Integer, db.ForeignKey('sd.id'), primary_key=True)
    hodnota = db.Column(db.String(50), nullable=True)
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
    tvar = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False)
    tvar_lower = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False, index=True)
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

    __mapper_args__ = {
        'polymorphic_identity': 'sl',
    }

    def exportuj(self, prvy_znak_upper):
        export = SlovoExport()
        export.id = self.id
        export.tvar = self.tvar
        export.tvar_lower = self.tvar_lower
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
        export.koncept_id = self.SlovnyDruh.koncept_id

        if export.koncept_id:
            export.koncept = Koncept.query.get(export.koncept_id).nazov

        export.sufix = self.SlovnyDruh.sufix
        export.prefix = self.SlovnyDruh.prefix
        export.vzor = self.SlovnyDruh.vzor

        if export.slovny_druh == "PREDLOZKA":
            predlozka = Predlozka.query.get(export.sd_id)
            export.zoznam_padov = predlozka.pady

        return export

    def exportuj_komplet(self, prvy_znak_upper):
        export = self.exportuj(prvy_znak_upper)

        if export.slovny_druh == "POD_M":
            pm = PodstatneMeno.query.get(self.sd_id)
            export.rod = pm.rod
            export.podrod = pm.podrod
            export.sloveso_id = pm.sloveso_id

            if pm.sloveso_id:
                slov = Sloveso.query.get(pm.sloveso_id)
                export.sloveso_tvar = slov.zak_tvar

                if slov.zvratnost:
                    export.sloveso_tvar += " " + slov.zvratnost

        elif export.slovny_druh == "PRID_M":
            prm = PridavneMeno.query.get(self.sd_id)
            export.sloveso_id = prm.sloveso_id

            if prm.sloveso_id:
                slov = Sloveso.query.get(prm.sloveso_id)
                export.sloveso_tvar = slov.zak_tvar

                if slov.zvratnost:
                    export.sloveso_tvar += " " + slov.zvratnost

            export.je_privlastnovacie = prm.je_privlastnovacie

        elif export.slovny_druh == "ZAMENO":
            zam = Zameno.query.get(self.sd_id)

        elif export.slovny_druh == "SLOVESO":
            s = Sloveso.query.get(self.sd_id)
            export.zvratnost = s.zvratnost
            export.je_negacia = s.je_negacia
            export.sloveso_id = s.pozitivne_sloveso_id

            if s.pozitivne_sloveso_id:
                slov = Sloveso.query.get(s.pozitivne_sloveso_id)
                export.sloveso_tvar = slov.zak_tvar

                if slov.zvratnost:
                    export.sloveso_tvar += " " + slov.zvratnost

        elif export.slovny_druh == "CISLOVKA":
            cis = Cislovka.query.get(self.sd_id)
            export.hodnota = cis.hodnota

        return export


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


class SlovesoView(db.Model):
    __table__ = create_view(
        name='sd_sloveso_v',
        selectable=sa.select(
            [
                Sloveso.sd_id.label('id'),
                SlovnyDruh.zak_tvar,
                SlovnyDruh.koren,
                Sloveso.pzkmen,
                SlovnyDruh.vzor,
                Sloveso.popis,
                Sloveso.zvratnost,
                Sloveso.vid,
                Sloveso.je_negacia,
                Sloveso.pozitivne_sloveso_id,
                Sloveso.zmenene,
                Sloveso.user_id,
            ],
            from_obj=Sloveso.__table__.join(SlovnyDruh, SlovnyDruh.id == Sloveso.sd_id)
        ),
        metadata=db.Model.metadata
    )


class SDVzor(db.Model):
    __tablename__ = 'sd_vzor'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    rod = db.Column(db.String(1), nullable=False)
    podrod = db.Column(db.String(1), nullable=True)
    vzor = db.Column(db.String(50), nullable=False)
    deklinacia = db.Column(db.String(500), nullable=False)
    alternacia = db.Column(db.String(50), nullable=True)
    sklon_stup = db.Column(db.String(50), nullable=False)
    popis = db.Column(db.String(500), nullable=True)

    def exportuj(self):
        export = VzorExport()
        export.id = self.id
        export.typ = self.typ
        export.vzor = self.vzor
        export.rod = self.rod
        export.podrod = self.podrod
        export.deklinacia = self.deklinacia
        export.alternacia = self.alternacia
        export.sklon_stup = self.sklon_stup
        export.popis = self.popis
        return export


class SDVzorTemp(db.Model):
    __tablename__ = 'sd_vzor_temp'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    rod = db.Column(db.String(1), nullable=False)
    podrod = db.Column(db.String(1), nullable=True)
    vzor = db.Column(db.String(50), nullable=False)
    deklinacia = db.Column(db.String(500), nullable=False)
    alternacia = db.Column(db.String(50), nullable=True)
    popis = db.Column(db.String(500), nullable=True)


class SDPrefixSufix(db.Model):
    __tablename__ = 'sd_prefix_sufix'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    prefix_sufix = db.Column(db.String(1), nullable=False)
    hodnota = db.Column(db.String(50), nullable=False)

    def exportuj(self):
        export = PrefixSufixExport()
        export.id = self.id
        export.typ = self.typ
        export.prefix_sufix = self.prefix_sufix
        export.hodnota = self.hodnota
        return export


class SlovoRozdiel(db.Model):
    __tablename__ = 'sl_rozdiel'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    sl_id = db.Column(db.Integer)
    vygen_status = db.Column(db.String(10), nullable=True)
    tvar = db.Column(db.String(500, collation='utf8mb4_bin'), nullable=False, index=True)
    anotacia = db.Column(db.String(10), nullable=True)
    rod = db.Column(db.String(1), nullable=True)
    podrod = db.Column(db.String(1), nullable=True)
    pad = db.Column(db.String(3), nullable=True)
    stupen = db.Column(db.String(1), nullable=True)
    sposob = db.Column(db.String(1), nullable=True)
    osoba = db.Column(db.String(1), nullable=True)
    cas = db.Column(db.String(1), nullable=True)
    pricastie = db.Column(db.String(1), nullable=True)
    cislo = db.Column(db.String(1), nullable=True)
    sd_id = db.Column('sd_id', db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'sl_rozdiel',
    }


class SlovnyDruhStat(db.Model):
    __tablename__ = 'sd_stat'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False, index=True)
    pocet = db.Column(db.Integer, nullable=True)


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
                sa.select([sa.func.count()], from_obj=SlovnyDruhSemantika).where(SlovnyDruhSemantika.sem_priznak_id ==
                                                                                 SemHierarchia.sem_id)
                    .label('pocet_slov'),
            ],
            from_obj=(
                SemHierarchia.__table__.join(sem1, sem1.id == SemHierarchia.sem_id)
                .outerjoin(sem2, sem2.id == SemHierarchia.rodic_id)
            )
        ),
        metadata=db.Model.metadata
    )


