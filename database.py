from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///appDB.db', echo=True)
Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	password = Column(String)
	
	def __repr__(self):
		return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)
