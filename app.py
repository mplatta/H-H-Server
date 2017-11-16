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
    if request.method == "OPTIONS":
        print("dupa")
        data = {
            "POST": {
                "description": "Check passed credentials.",
                "parameters": {
                    "email": {
                        "type": "string",
                        "description": "Users e-mail address."
                    },
                    "password": {
                        "type": "string",
                        "description": "Users password."
                    }
                },
                "example": {
                    "email": "admin@localhost.org",
                    "password": "5tr0ngp4ssw0rd"
                },
                "response": {
                    "success": {
                        "type": "boolean",
                        "description": "True if found user matching email and password. False otherwise."
                    },
                    "userId": {
                        "type": "integer",
                        "description": "Users ID from database. Null/None if failed to match."
                    },
                    "nickName": {
                        "type": "string",
                        "description": "Users nick name form database. Null/None if failed to match."
                    }
                }
            }
        }
        print(data)
        return jsonify(data)

    if request.method == "POST":
        email = str(request.form["email"])
        password = str(request.form["password"])
        user = dbControl.login(email, password)
        if user:
            data = {"success": True, "userId": user.id, "nickName": user.login}
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
        userid = str(request.form["userid"])
        start_delay = int(request.form["start_delay"])
        privacy = int(request.form["privacy"])
        if dbControl.creategame(userid, start_delay, privacy):
            data = {"Success": True, "userid": userid}
        else:
            data = {"Success": False, "email": None}
        return jsonify(data)
    elif request.method == 'GET':
        # seekerLat = double(request.form["seekerLat"])
        # seekerLon = double(request.form["seekerLon"])
        # radius = double(request.form["radius"])
        data = {}
        return jsonify(data)


@app.route("/api/friends", methods=["POST", "GET"])
def friends():
    if request.method == "OPTIONS":
        data = {}
        return jsonify(data)

    if request.method == 'POST':
        # add friend to database
        pass
    elif request.method == 'GET':
        # get friend list from database
        pass


Blog.register(app)
articles = Blog.getArticles()


if __name__ == '__main__':
    # app.run(debug=False, host='42.0.139.255')
    app.run(debug=True, host='localhost')
