from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB"]
db = SQLAlchemy(app)

class Rank(db.Model):
    __tablename__ = "ranks"
    userid = db.Column(db.String(30), primary_key=True)
    rank = db.Column(db.Integer())
db.create_all()

def rankup(id):
    id = str(id)
    a = db.session.query(Rank).get(id)
    if a:
        a.rank += 1
        db.session.add(a)
        db.session.commit()
    else:
        a = Rank(userid=id, rank=1)
        db.session.add(a)
        db.session.commit()

def getrank(id):
    id = str(id)
    a = db.session.query(Rank).get(id)
    if a:
        return a.rank
    else:
        return 0
