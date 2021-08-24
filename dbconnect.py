from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime
import os

db = create_engine(os.environ.get("DB"))
db = db.connect()
metadata = MetaData()

aboba = Table('rank', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('rank', Integer()))
def rankup(id):
 try:
  db.execute(aboba.update().where(aboba.c.id == id).values(rank = db.execute(aboba.select().where(aboba.c.id == id)).fetchone()[1]+1))
 except TypeError:
  db.execute(aboba.insert().values(id=id, rank=1))
def getrank(id):
 return(db.execute(aboba.select().where(aboba.c.id == id)).fetchone()[1])