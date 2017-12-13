from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
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
        return "<User(login='%s', id='%s', password='%s')>" % (self.login, self.id, self.password)


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


class Friend(Base):
    __tablename__ = 'Friends'
    user1 = Column(Integer, ForeignKey(User.id), primary_key=True)
    user2 = Column(Integer, ForeignKey(User.id), primary_key=True)
    UniqueConstraint(user2, user1, name="uniUsers")

    def __repr__(self):
        return "<Friendship between '%s' and '%s')>" % (self.user1, self.user2)


class Waypoint(Base):
    __tablename__ = "Waypoints"
    id = Column(Integer, primary_key=True)
    pos_X = Column(Float)
    pos_Y = Column(Float)
    pos_Z = Column(Float)
    isActive = Column(Boolean)
    riddle = Column(Integer, ForeignKey(Riddle.id), default=0)


class Game(Base):
    __tablename__ = 'Games'
    id = Column(Integer, primary_key=True)
    host = Column(Integer, ForeignKey(User.id))
    start_data = Column(Date)
    end_data = Column(Date)
    point = Column(Integer, ForeignKey(Waypoint.id))
    isActive = Column(Boolean)


class Player(Base):
    __tablename__ = "Players"
    idUser = Column(Integer, ForeignKey(User.id), primary_key=True)
    idGames = Column(Integer, ForeignKey(Game.id), primary_key=True)
    # isPursuiting: true dla goniacego, false dla uciekajacego
    isPursuiting = Column(Boolean)
    isReady = Column(Boolean)


class Path(Base):
    __tablename__ = "Paths"
    id = Column(Integer, primary_key=True)
    idWaypoint = Column(Integer, ForeignKey(Waypoint.id))


class GameProperty(Base):
    __tablename__ = "GameProperties"
    start_delay = Column(Integer)
    privacy = Column(Integer)
    idGames = Column(Integer, ForeignKey(Game.id), primary_key=True)
    startPath = Column(Integer, ForeignKey(Path.id))


class RiddleInGame(Base):
    __tablename__ = "RiddlesInGame"
    idRiddles = Column(Integer, ForeignKey(Riddle.id), primary_key=True)
    idGames = Column(Integer, ForeignKey(Game.id), primary_key=True)
    noRiddle = Column(Integer, autoincrement=True)


Base.metadata.create_all(engine)


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

        def getId(friend_login):
            query = session.query(User).filter(User.login == friend_login)
            friend = query.first()
            print(friend)
            if friend is not None:
                return friend.id
            else:
                return False

        # willDuplicate check if relation already exist but other way round
        # returns True if relation exist and shouldn't be made
        # and False if not and cane be made
        def willDuplicate():
            query = session.query(Friend).filter(Friend.user1 == friend_id).filter(Friend.user2 == host)
            result = query.first()
            if result:
                return True
            else:
                return False

        friend_id = getId(friend_login)
        if not friend_id:
            return False
        elif int(friend_id) == int(host):
            return False

        if not willDuplicate():
            new_relation = Friend(user1=host, user2=friend_id)
            session.add(new_relation)
            try:
                session.commit()
            except IntegrityError:
                return False
            return True
        else:
            return False

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

    def creategame(userid, start_delay, privacy, pos_x, pos_y):
        global session
        game = Game(host=userid)
        session.add(game)
        session.flush()
        game_property = GameProperty(
            start_delay=start_delay, privacy=privacy, idGames=game.id)
        session.add(game_property)
        session.flush()
        player = Player(idUser=userid, idGames=game.id, isPursuiting=False, isReady=True)
        session.add(player)
        session.commit()
        return game.id

    def getGames():
        global session
        query = session.query(Game, Waypoint, GameProperty).filter(
            Game.point == Waypoint.id).filter(GameProperty.idGames == Game.id).all()
        print(query)

        # game list with name, distance, id

    # Checked, working
    def getFriends(userid):
        global session
        query = session.query(Friend).filter(
            (Friend.user1 == userid) | (Friend.user2 == userid)).all()
        friends = [{"id": line.user1} if not line.user1 == userid else {"id": line.user2} for line in query]
        for friend in friends:
            query_username = session.query(User.login).filter(User.id == friend["id"])
            friend["login"] = query_username.first()[0]
        return friends
        # friend list of friends

    def joinGame(userId, gamesId):
        global session
        player = Player(idUser=userId, idGames=gamesId, isPursuiting=1, isReady=0)
        session.add(player)
        session.commit()
        return True

    def isPlayer(playerId):
        global session
        query = session.query(Player).filter(Player.idUser == playerId).all()
        print(query)

    def leaveGame(user, game):
        global session
        player = session.query(Player).filter(Player.idUser == user).filter(Player.idGames == game).one()
        session.delete(player)
        session.commit()
        return True

    def getPlayers(gameId):
        global session
        players = session.query(Player).filter(Player.idGames == gameId).all()
        return players

    def setReady(user, game):
        global session
        player = session.query(Player).filter(Player.idUser == user).filter(Player.idGames == game).one()
        player.isReady = True
        session.commit()
        return True

    def setNotReady(user, game):
        global session
        player = session.query(Player).filter(Player.idUser == user).filter(Player.idGames == game).one()
        player.isReady = False
        session.commit()
        return True


# dbControl.getGames()
# dbControl.addFriend(1000, "mplatta")
# print(dbControl.creategame(userid=1000, start_delay=2, privacy=0, pos_x=0, pos_y=0))
# dbControl.isPlayer(1000)
# print(dbControl.setReady(1002, 6))
