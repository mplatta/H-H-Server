from flask import Flask, request, render_template, jsonify, url_for
from blog import NewsLogger
from database import dbControl

# from flask_restful import Resource, Api
# import sqlalchemy

app = Flask(__name__)
app.secret_key = 'some_secret'
# api = Api(app)

valid = True

Blog = NewsLogger()

articles = Blog.getArticles()


@app.route("/")
def status():
    global valid
    global articles
    problems = ["Cannot connect to database"]
    return render_template("info.html", valid=valid, problems=problems, articles=articles)


@app.route("/admin", methods=["POST", "GET"])
def administrationView():
    global valid
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


@Blog.register()
@app.route(rule="/api/login", methods=["POST"])
def login():
    global Blog
    global valid
    if request.method == "POST":
        email = str(request.form["email"])
        password = str(request.form["password"])
        user = dbControl.login(email, password)
        if user:
            data = {"success": True, "userId": user.id, "nickName": user.login}
        else:
            data = {"success": False, "userId": None, "nickName": None}

        return jsonify(data)


@Blog.register()
@app.route("/api/register", methods=["POST"])
def register():
    global valid
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


@Blog.register()
@app.route("/api/resetpswd", methods=['POST'])
def resetPassword():
    global valid
    if request.method == 'POST':
        email = str(request.form["email"])
        if dbControl.resetPassword(email):
            data = {"Success": True, "email": email}
        else:
            data = {"Success": False, "email": None}
        return jsonify(data)


@Blog.register()
@app.route("/api/games", methods=["POST", "GET"])
def games():
    global valid
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
        # get games nearby form database
        pass


@Blog.register()
@app.route("/api/friends", methods=["POST", "GET"])
def friends():
    if request.method == 'POST':
        # add friend to database
        pass
    elif request.method == 'GET':
        # get friend list from database
        pass


if __name__ == '__main__':
    # app.run(debug=False, host='42.0.139.255')
    app.run(debug=True, host='localhost')
