from app.db.main import *


class Kt2mTemplate(db.Model):
    __tablename__ = 'kt2m_template'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'}
    id = db.Column(db.Integer, primary_key=True)
    nazov = db.Column(db.String(2000), nullable=False)
    obsah = db.Column(db.Text(4000000000), nullable=False)
    kod = db.Column(db.String(2000), nullable=True)
