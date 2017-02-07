from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import db

# declarative base for our declarative models
# it knows everything about our models so use it
# when you need metadata about models created here
Base = declarative_base()


class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, nullable=False)
	username = Column(String(250))


class Update(Base):
	__tablename__ = 'update'

	id = Column(Integer, primary_key=True)
	lastoffset = Column(Integer)