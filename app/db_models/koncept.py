from app.db_models.main import *


class Koncept(db.Model):
    __tablename__ = 'kc'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    nazov = db.Column(db.String(20), nullable=False, index=True)
    popis_obsah = db.Column(db.Text(4000000000))
    silny_popis = db.Column(db.Text(4000000000))


class KonceptAtribut(db.Model):
    __tablename__ = 'kc_at'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    kc_id = db.Column('kc_id', db.Integer, db.ForeignKey('kc.id'))
    typ = db.Column(db.String(20), nullable=False)
    dlzka = db.Column('dlzka', db.Integer, nullable=True)
    kardinalita = db.Column(db.String(1), nullable=False)
    vlastnost_koncept_id = db.Column('at_kc_id', db.Integer, db.ForeignKey('kc.id'))


class KonceptHierarchia(db.Model):
    __tablename__ = 'kc_hier'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    kc_id = db.Column('kc_id', db.Integer, db.ForeignKey('kc.id'))
    rodic_kc_id = db.Column('rodic_kc_id', db.Integer, db.ForeignKey('kc.id'))
    poradie = db.Column('poradie', db.Integer, nullable=True)


