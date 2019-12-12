# ~/app/models/smartpixldata.py
from app import db


class SmartPixlData(db.Model):
    __table__name = "smartpixl_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    smartpixl_recordId = db.Column(db.Integer, nullable=False)
    companyId = db.Column(db.Integer, nullable=False, index=True)
    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))
    email = db.Column(db.String(120))
    email_source = db.Column(db.String(25))
    email_status = db.Column(db.String(10))
    smartpixl_data = db.Column(db.Text)
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
