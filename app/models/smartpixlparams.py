# ~/app/models/smartpixlparams.py
from app import db


class SmartPixlParams(db.Model):
    __table__name = "smartpixl_params"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.Integer, unique=True, nullable=False, index=True)
    pixlId = db.Column(db.Integer, unique=True, nullable=False)
    domain = db.Column(db.String(60), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
