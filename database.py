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
        return "<User(login='%s', id='%s')>" % (self.login, self.id)


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
    idUser = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True)
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
    idWaypoint = Column(Integer, ForeignKey(Waypoint.id), default=0)


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

        def isHost():
            r = session.query(Game).filter_by(host=userid).first()
            if r:
                return r
            else:
                return False

        r = isHost()
        if r:
            return r.id

        game = Game(host=userid, isActive=False)
        session.add(game)
        session.flush()
        game_property = GameProperty(
            start_delay=start_delay, privacy=privacy, idGames=game.id)
        session.add(game_property)
        session.flush()
        try:
            player = Player(idUser=userid, idGames=game.id, isPursuiting=False, isReady=False)
            session.add(player)
            session.commit()
            return game.id
        except Exception:
            return -1

    def getGames():
        global session
        query = session.query(Game).filter(Game.isActive is False).all()
        return query

    def getOneGame(gameId):
        global session
        game = session.query(Game).filter_by(id=gameId).one()
        return game

    # Checked, working
    def getFriends(userid):
        global session
        query = session.query(Friend).filter(
            (Friend.user1 == userid) | (Friend.user2 == userid)).all()
        friends = [{"id": line.user1} if not line.user1 == userid else {"id": line.user2} for line in query]
        for friend in friends:
            query_username = session.query(User.login).filter(User.id == friend["id"])
            query_ishost = session.query(Game).filter(Game.isActive == 0).filter(Game.host == friend["id"]).first()
            friend["login"] = query_username.first()[0]
            friend["gameId"] = query_ishost.id if query_ishost is not None else 0
        return friends
        # friend list of friends

    def isPlayer(playerId):
        global session
        query = session.query(Player).filter_by(idUser=playerId).first()
        if query:
            return True
        else:
            return False

    def joinGame(userId, gamesId):
        global session
        if dbControl.isPlayer(userId) is False:
            player = Player(idUser=userId, idGames=gamesId, isPursuiting=1, isReady=0)
            session.add(player)
            session.commit()
            return True
        else:
            return False

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

    def getLoginByID(userId):
        global session
        login = session.query(User).filter_by(id=userId).one().login
        return login

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

    def getRiddle():
        global session
        riddles = session.query(Riddle).count()
        from random import randint
        riddleId = randint(1, riddles)
        riddle = session.query(Riddle).filter_by(id=riddleId).one()
        return riddle

    def pushWayPoint(gameId, pos_x, pos_y, riddleId):
        global session

        waypoint = Waypoint(pos_X=pos_x, pos_Y=pos_y, pos_Z=0.0, isActive=False)
        session.add(waypoint)
        session.flush()
        if riddleId is not None:
            record = RiddleInGame(idGames=gameId, idRiddles=riddleId, idWaypoint=waypoint.id)
            session.add(record)
            session.flush()
        try:
            game = session.query(Game).filter_by(id=gameId).one()
            game.point = waypoint.id
            session.commit()
        except Exception:
            return False

    def resetGames():
        global session
        session.query(GameProperty).delete()
        session.query(Player).delete()
        session.query(Game).delete()
        session.query(Waypoint).delete()
        session.commit()


# print(dbControl.getGames())
# dbControl.addFriend(1001, "awejler")
# print(dbControl.creategame(userid=1000, start_delay=2, privacy=0, pos_x=0, pos_y=0))
# dbControl.isPlayer(1000)
# print(dbControl.setReady(1002, 6))
# print(dbControl.getFriends(1001))
# print(dbControl.getLoginByID(1000))
# print(dbControl.getPlayers(1))
# print(dbControl.joinGame(1002, 1))
# print(dbControl.getRiddle())
# dbControl.resetGames()
dbControl.pushWayPoint(1, 2.0, 3.44, 1)
