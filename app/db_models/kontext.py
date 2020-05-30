from app.db_models.main import *
from app.db_models.user import *


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
