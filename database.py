from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.init_app(app)
class Rank(db.Model):
    __tablename__ = "nb_ranks"
    userid = db.Column(db.String(30), primary_key=True)
    rank = db.Column(db.Integer())
class Server(db.Model):
    __tablename__ = "nb_servers"
    serverid = db.Column(db.String(30), primary_key=True)
    prefix = db.Column(db.String(5))
    adminroleid = db.Column(db.String(30))
    premium = db.Column(db.Boolean())
class Warn(db.Model):
    __tablename__ = "nb_warns"
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.String(30))
    serverid = db.Column(db.String(30))
    text = db.Column(db.Text())
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

def getServerSettings(id):
    id = str(id)
    a = db.session.query(Server).get(id)
    if a:
        return { "serverID": int(id),
                 "prefix": a.prefix,
                 "adminRoleID": a.adminroleid,
                 "premium": a.premium }
    else:
        a = Server(serverid=id, prefix="n!", adminroleid=None, premium=False)
        db.session.add(a)
        db.session.commit()
        return getServerSettings(id)

def getwarns(serverid,userid):
    lst = db.session.query(Warn).filter(Warn.serverid == str(serverid) and Warn.userid == str(userid)).all()
    lst2 = []
    for warn in lst:
        lst2.append(f"ID: **{warn.id}** \nText: **{warn.text}**")
    return lst2

def mkwarn(serverid,userid,roleid,txt):
    ss = getServerSettings(serverid)
    if ss["adminRoleID"] == roleid:
        w = Warn(id=db.session.query(Warn).all()[-1].id+1, serverid=serverid, userid=userid, text=txt)
        db.session.add(w)
        db.session.commit()
        return "OK"
    elif not ss["adminRoleID"]:
        return "I can't confirm that you are an admin. Server owner must specify admin role using n!set_admin_role <role ID>."
    else:
        return "Sorry, you are not an admin."

def setServerSettings(ss):
    ss2 = db.session.query(Server).get(ss["serverid"])
    ss2.prefix = ss["prefix"]
    ss2.adminroleid = ss["adminRoleID"]
    ss2.premium = ss["premium"]
    db.session.add(ss2)
    db.session.commit()
def lsguilds_id():
    tmp = []
    for id in Server.query.all():
        tmp.append(id.serverid)
    return tmp
#def delwarn(id, serverid, roleid):
#  if getServerSettings(serverid)["adminRoleID"] == roleid:
    
