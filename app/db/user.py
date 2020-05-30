from app.db.main import *


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
    je_admin_konceptov = db.Column(db.String(1), nullable=True)

    def nastav_heslo(self, password):
        self.password = generate_password_hash(password)

    def skontroluj_heslo(self, password):
        return check_password_hash(self.password, password)


