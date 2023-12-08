# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bone(db.Model):
    __tablename__ = 'tblbones'
    boneID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
