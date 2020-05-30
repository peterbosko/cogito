from app.db.main import *
from app.db.user import *


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
