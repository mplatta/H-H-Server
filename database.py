from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///appDB.db', echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
	__tablename__ = 'Users'
	id = Column(Integer, primary_key=True)
	login = Column(String)
	password = Column(String)
	email = Column(String)
	
	def __repr__(self):
		return "<User(login='%s', password='%s')>" % (self.login, self.password)

# class Friend(Base):
# 	__tablename__ = 'Friends'
# 	user1 = Column(Integer)
# 	user2 = Column(Integer)

# class Game(Base):
# 	__tablename__ = 'Games'
# 	id = Column(Integer, primary_key=True)
# 	properties = Column(String)
# 	host = Column(Integer)
# 	start_data = Column(Date)
# 	end_data = Column(Date)
# 	path = Column(String)

# class Player(Base):
# 	__tablename__="Players"
# 	idUser = Column(Integer)
# 	idGames = Column(Integer)

# class Riddle(Base):
# 	__tablename__="Riddles"
# 	id = Column(Integer, primary_key=True)
# 	text = Column(String)
# 	answer = Column(String)

# Base.metadata.create_all(engine)

def checkCredentials(login, password):
	global session
	query = session.query(User).filter(User.login==login, User.password==password)
	if query.first():
		return True
	else:
		return False

