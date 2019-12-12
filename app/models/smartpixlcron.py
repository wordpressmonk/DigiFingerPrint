# ~/app/models/smartpixelcron.py
from app import db


class SmartPixlCron(db.Model):
    __table__name = "smartpixl_cron_time"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
