from flask import Flask, request, render_template, jsonify
from blog import NewsLogger
from database import dbControl

# from flask_restful import Resource, Api
# import sqlalchemy

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route("/")
def status():
    global valid
    YOUR_API_KEY = ' AIzaSyCk_JkSZuO6xgIckOxi9CXL2l3dO3T0-MY '
    latitude = 18.6185821
    longitude = 54.371757
    return render_template("base.html", key=YOUR_API_KEY, latitude=latitude, longitude=longitude)


@app.route("/admin", methods=["POST", "GET"])
def administrationView():
    if app.debug:
        if request.method == "POST":
            password = request.form['password']
            if password == "super":
                message = "password correct"
            else:
                message = "password incorrect"
            return render_template(
                'message.html',
                valid=valid,
                message=message
            )
        else:
            return render_template('administration.html', valid=valid)
    else:
        return render_template('administration.html', valid=valid)


@app.route(rule="/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = str(request.form["email"])
        password = str(request.form["password"])
        user = dbControl.login(email, password)
        if user:
            data = {"success": True, "userId": user.id, "nickName": user.login}
            print(data)
        else:
            data = {"success": False, "userId": None, "nickName": None}

        return jsonify(data)


@app.route("/api/register", methods=["POST"])
def register():
    if request.method == "OPTIONS":
        data = {}
        return jsonify(data)

    if request.method == "POST":
        print(request.form)
        nickName = str(request.form["nickName"])
        password = str(request.form["password"])
        email = str(request.form["email"])
        result = dbControl.checkAvailability(nickName, email)
        if result == 1:
            dbControl.registerUser(nickName, password, email)
            data = {"mailSuccess": True, "loginSuccess": True}
        elif result == 0:
            data = {"mailSuccess": False, "loginSuccess": False}
        elif result == -1:
            data = {"mailSuccess": False, "loginSuccess": False}
        return jsonify(data)


@app.route("/api/resetpswd", methods=['POST'])
def resetPassword():
    if request.method == "OPTIONS":
        data = {}
        return jsonify(data)

    if request.method == 'POST':
        email = str(request.form["email"])
        if dbControl.resetPassword(email):
            data = {"Success": True, "email": email}
        else:
            data = {"Success": False, "email": None}
        return jsonify(data)


@app.route("/api/games", methods=["POST", "GET"])
def games():
    if request.method == "OPTIONS":
        data = {}
        return jsonify(data)

    if request.method == 'POST':
        userid = str(request.form["userId"])
        start_delay = int(request.form["start_delay"])
        privacy = int(request.form["privacy"])
        gameId = dbControl.creategame(userid, start_delay, privacy, 0.0, 0.0)
        if gameId is not False:
            data = {"Success": True, "gameId": gameId}
        else:
            data = {"Success": False, "email": None}
        return jsonify(data)
    elif request.method == 'GET':
        games = dbControl.getGames()
        data = {
            "games": []
        }
        for game in games:
            if not game.isActive:
                json = {
                    "id": game.id,
                    "host": game.host,
                    "start_date": game.start_date,
                    "privacy": game.privacy,
                }
            data["games"].append(json)
        # seekerLat = float(request.form["seekerLat"])
        # seekerLon = float(request.form["seekerLon"])
        # radius = float(request.form["radius"])
        return jsonify(data)


@app.route("/api/games/one", methods=["POST"])
def getOneGame():
    if request.method == "POST":
        gameId = request.forms["gameId"]
        game = dbControl.getOneGame(gameId)
        data = {
            "id": game.id,
            "host": game.host,
            "start_date": game.start_date,
            "isActive": game.isActive,
        }
        return jsonify(data)
    return jsonify({"succsess": False})


@app.route("/api/games/leave", methods=["GET"])
def leave():
    if request.method == "GET":
        player = request.args.get("userId")
        game = request.args.get("gameId")
        r = dbControl.leaveGame(player, game)
        if r:
            data = {
                "success": True,
            }
        else:
            data = {
                "success": False,
            }
        return jsonify(data)


@app.route("/api/games/lobby", methods=["POST"])
def checkLobby():
    if request.method == "POST":
        gameId = str(request.form["gameId"])
        players = dbControl.getPlayers(gameId)
        if len(players) > 0:
            ready = True
        else:
            ready = False
        data = {
            "players": []
        }

        for player in players:
            ready *= player.isReady
            json = {
                "userId": player.idUser,
                "gameId": player.idGames,
                "isPursuiting": player.isPursuiting,
                "isReady": player.isReady,
                "login": dbControl.getLoginByID(player.idUser)
            }
            data["players"].append(json)
        data["ready"] = bool(ready)
        return jsonify(data)


@app.route("/api/games/setready", methods=["POST"])
def setReady():
    if request.method == "POST":
        user = int(request.form["userId"])
        game = int(request.form["gameId"])
        r = dbControl.setReady(user, game)
        data = {
            "success": r
        }
        return jsonify(data)


@app.route("/api/games/notready", methods=["POST"])
def getNotReady():
    if request.method == "POST":
        user = int(request.form["userId"])
        game = int(request.form["gameId"])
        r = dbControl.setNotReady(user, game)
        data = {
            "success": r
        }
        return jsonify(data)


@app.route("/api/games/join", methods=["POST"])
def joinGame():
    if request.method == "POST":
        userId = int(request.form["userId"])
        gameId = int(request.form["gameId"])
        r = dbControl.joinGame(userId, gameId)
        data = {
            "success": r,
        }
        return jsonify(data)


@app.route("/api/friends", methods=["POST", "GET"])
def friends():
    if request.method == 'POST':
        host = int(request.form["userId"])
        friend = request.form["nickName"]
        if dbControl.addFriend(host, friend):
            data = {"success": True}
        else:
            data = {"success": False}
        return jsonify(data)

    elif request.method == 'GET':
        userid = int(request.args.get("userId"))
        friendsList = dbControl.getFriends(userid)
        data = {
            "message": "List of users friends.",
            "count": len(friendsList),
            "friendsList": friendsList
        }
        return jsonify(friendsList)


@app.route("/api/setWaypoint", methods=["POST"])
def Waypoint():
    if request.method == 'POST':
        gameId = int(request.form["gameId"])
        pos_x = float(request.form["pos_x"])
        pos_y = float(request.form["pos_y"])
        if str(request.form["riddle"]) == "True":
            riddle = dbControl.getRiddle()
            dbControl.pushWayPoint(gameId, pos_x, pos_y, riddle.id)
        else:
            riddle = None
            dbControl.pushWayPoint(gameId, pos_x, pos_y, None)
        data = {
            "success": True,
        }
        return jsonify(data)


@app.route("/api/games/checkpoint", methods=["POST"])
def checkpoint():
    if request.method == 'POST':
        gameId = int(request.form["gameId"])
        r = dbControl.checkpoint(gameId)
        if r:
            isRiddle = True
            riddle = dbControl.getRiddle(r.idRiddles)
            pos_x, pos_y = dbControl.getCoords(r.idWaypoint)
        else:
            isRiddle = False
            pos_x, pos_y = dbControl.getLastWaypoint(gameId)

        data = {
            "pos_x": pos_x,
            "pos_y": pos_y,
            "flag": isRiddle,
        }
        if isRiddle:
            data["riddle"] = {
                "text": riddle.text,
                "answer": riddle.answer,
                "optionA": riddle.optionA,
                "optionB": riddle.optionB,
                "optionC": riddle.optionC,
                "optionD": riddle.optionD,
            }
        return jsonify(data)


@app.route("/api/games/updateQueue", methods=["POST"])
def ridRiddle():
    if request.method == 'POST':
        idRiddle = int(request.form["idRiddle"])
        r = dbControl.ridRiddle(idRiddle)


if __name__ == '__main__':
    app.run(debug=False, host='42.0.139.255')
    # app.run(debug=True, host='localhost')
