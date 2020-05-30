from app.db.main import *
from app.db.slovny_druh import *


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


class SlovnyDruhSemantika(db.Model):
    __tablename__ = 'sd_sem'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    sd_id = db.Column(db.Integer, db.ForeignKey("sd.id"), nullable=True, index=True)
    sem_priznak_id = db.Column(db.Integer, db.ForeignKey("sem.id"), nullable=True, index=True)
    sem_priznak = relationship("Semantika", foreign_keys=[sem_priznak_id])
    SlovnyDruh = relationship("SlovnyDruh", foreign_keys=[sd_id], back_populates="sem_priznaky")


