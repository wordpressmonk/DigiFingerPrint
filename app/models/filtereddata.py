# ~/app/models/filtereddata.py
from app import db


class FilteredData(db.Model):
    __table__name = "filtered_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.Integer, nullable=False, index=True)
    smartpixl_recordId = db.Column(db.Integer, nullable=False)
    smartpixl_date = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))
    email = db.Column(db.String(120))
    email_source = db.Column(db.String(25))
    email_status = db.Column(db.String(10))
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
