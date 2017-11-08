from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///appDB.db', echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)

    def __repr__(self):
        return "<User(login='%s', password='%s')>" % (self.login, self.password)


class Friend(Base):
    __tablename__ = 'Friends'
    user1 = Column(Integer, ForeignKey(User.id), primary_key=True)
    user2 = Column(Integer, ForeignKey(User.id), primary_key=True)


class Game(Base):
    __tablename__ = 'Games'
    id = Column(Integer, primary_key=True)
    host = Column(Integer, ForeignKey(User.id))
    start_data = Column(Date)
    end_data = Column(Date)


class Player(Base):
    __tablename__ = "Players"
    idUser = Column(Integer, ForeignKey(User.id), primary_key=True)
    idGames = Column(Integer, ForeignKey(Game.id), primary_key=True)


class Riddle(Base):
    __tablename__ = "Riddles"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    answer = Column(String)
    optionA = Column(String)
    optionB = Column(String)
    optionC = Column(String)
    optionD = Column(String)
    author = Column(Integer, ForeignKey(User.id))


class GameProperty(Base):
    __tablename__ = "GameProperties"
    start_delay = Column(Integer)
    privacy = Column(Integer)
    idGames = Column(Integer, ForeignKey(Game.id), primary_key=True)


class RiddleInGame(Base):
    __tablename__ = "RiddlesInGame"
    idRiddles = Column(Integer, ForeignKey(Riddle.id), primary_key=True)
    idGames = Column(Integer, ForeignKey(Game.id), primary_key=True)

# Base.metadata.create_all(engine)


class dbControl:
    def login(email, password):
        global session
        query = session.query(User).filter(
            User.email == email, User.password == password)
        user = query.first()
        if user:
            return user
        else:
            return False

    def registerUser(login, password, email):
        global session
        new_user = User(login=login, password=password, email=email)
        session.add(new_user)
        session.commit()
        return True

    def checkAvailability(login, email):
        global session
        query = session.query(User).filter(User.login == login)
        result = query.first()
        if result:
            loginOK = False
        else:
            loginOK = True
        query = session.query(User).filter(User.email == email)
        result = query.first()
        if result:
            emailOK = False
        else:
            emailOK = True

        if emailOK and loginOK:
            return 1
        if not emailOK and not loginOK:
            return 0
        if not emailOK:
            return -1

    def addFriend(host, friend_login):
        global session
        new_relation = Friend(user1=host, user2=friend_login)
        session.add(new_relation)
        session.commit()
        return True

    def addRiddle(text, answer, optionA, optionB, optionC, optionD, author):
        global session
        new_riddle = Riddle(text=text, answer=answer, optionA=optionA,
                            optionB=optionB, optionC=optionC, optionD=optionD, author=author)
        session.add(new_riddle)
        session.commit()
        return True

    def resetPassword(email):

        def generate():
            print("set new password for", email, " as ftims123")
            return "ftims123"

        global session
        query = session.query(User).filter(User.email == email)
        user = query.first()
        if user:
            user.password = generate()
            session.flush()
            session.commit()
            return True
        else:
            return False

    def creategame(userid, start_delay, privacy):
        global session
        game = Game(host=userid)
        session.add(game)
        session.flush()
        game_property = GameProperty(
            start_delay=start_delay, privacy=privacy, idGames=game.id)
        session.add(game_property)
        session.flush()
        player = Player(idUser=userid, idGames=game.id)
        session.add(player)
        session.commit()
        return True
