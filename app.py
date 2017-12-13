from flask import Flask, request, render_template, jsonify
from blog import NewsLogger
from database import dbControl

# from flask_restful import Resource, Api
# import sqlalchemy

app = Flask(__name__)
app.secret_key = 'some_secret'
# api = Api(app)

Blog = NewsLogger()


@app.route("/")
def status():
    global valid
    global articles
    return render_template("info.html", articles=articles)


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

        # seekerLat = float(request.form["seekerLat"])
        # seekerLon = float(request.form["seekerLon"])
        # radius = float(request.form["radius"])
        data = {}
        return jsonify(data)


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


@app.route("/api/games/lobby", methods=["GET"])
def checkLobby():
    if request.method == "GET":
        gameId = request.args.get("gameId")
        players = dbControl.getPlayers(gameId)
        if len(players) > 1:
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
            }
            data["players"].append(json)
        data["ready"] = ready
        return jsonify(data)


@app.route("/api/games/getready", methods=["POST"])
def getReady():
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
        host = request.form["userId"]
        friend = request.form["nickName"]
        if dbControl.addFriend(host, friend):
            data = {"success": True}
        else:
            data = {"success": False}
    elif request.method == 'GET':
        userid = int(request.args.get("userId"))
        friendsList = dbControl.getFriends(userid)
        data = {
            "message": "List of users friends.",
            "count": len(friendsList),
            "friendsList": friendsList
        }
    return jsonify(friendsList)


Blog.register(app)
articles = Blog.getArticles()


if __name__ == '__main__':
    app.run(debug=False, host='42.0.139.255')
    # app.run(debug=True, host='localhost')
