from datetime import datetime

import sqlalchemy as sqa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask_login import UserMixin

url = 'postgresql://pbntciav:i2SRiKluRqf6WtifDKplLNfz6p9lKT_1@floppy.db.elephantsql.com/pbntciav'
engine = sqa.create_engine(url, echo=True)
Base = declarative_base()

# # create a Session
Session = sessionmaker(bind=engine)
session = Session()


class IncomeExpenses(Base):
    __tablename__ = 'api_sold'

    id = sqa.Column(sqa.Integer, primary_key=True)
    type = sqa.Column(sqa.String(30), default='income', nullable=False)
    category = sqa.Column(sqa.String(30), default='rent', nullable=False)
    date = sqa.Column(sqa.DateTime, default=datetime.utcnow, nullable=False)
    amount = sqa.Column(sqa.Integer, nullable=False)

    def __repr__(self):
        return "IncomeExpenses(id = {}, type = {}, category = {}, date = {}, amount = {})".format(
            self.id,
            self.type,
            self.category,
            self.date,
            self.amount)


class User(Base):
    id = sqa.Column(sqa.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = sqa.Column(sqa.String(100), unique=True)
    password = sqa.Column(sqa.String(100))
    name = sqa.Column(sqa.String(1000))

