from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import datetime
import pickle
# from hashlib import sha256
from database import dbControl

# from flask_restful import Resource, Api
# import sqlalchemy

app = Flask(__name__)
app.secret_key = 'some_secret'
# api = Api(app)

valid = True


# class Stats:

#     def __init__(self):
#         self.path = 'timestamps'
#         try:
#             self.log = self.readTimestamps()
#         except Exception as e:
#             self.log = {'repair': [], 'broke': []}

#     def readTimestamps(self):
#         with open(self.path, 'rb') as f:
#             log = pickle.load(f)
#         return log

#     def writeTimestamps(self):
#         with open(self.path, 'wb') as f:
#             pickle.dump(self.log, f)

#     def getStats(self):

#         def format(timedelta):
#             table = str(timedelta).split(':')
#             table = table[0].split(' ') + table[1:]
#             string = table[0] + ' hours ' + table[1].replace(
#                 '00', '0') + ' minutes and ' + str(int(float(table[2]))) + ' seconds'
#             return string

#         global valid
#         if len(self.log['repair']) > 0 and len(self.log['broke']) > 0:
#             brokenTime = self.log['repair'][-1] - self.log['broke'][-1]
#             validTime = self.log['broke'][-1] - self.log['repair'][-1]
#             try:
#                 if self.log['highscore'] < validTime:
#                     self.log['highscore'] = validTime
#             except Exception as e:
#                 self.log['highscore'] = validTime

#             if valid:
#                 flash('Server was down for ' + format(brokenTime))
#             else:
#                 flash('Server has stopped after ' +
#                       format(validTime) + ' of continous work.')
#             flash(format(self.log['highscore']) +
#                   ' is actual record of server performence.')
#         else:
#             flash('Logs not found.')


# STATS = Stats()


@app.route("/")
def status():
    global valid
    problems = ["Cannot connect to database"]
    return render_template("base.html", valid=valid, problems=problems)


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


# @app.route('/switch')
# def switchValid():
#     global valid
#     # global STATS
#     valid = not valid
#     if valid:
#         STATS.log['repair'].append(datetime.datetime.now())
#         flash('Successfully repaired server.')
#     else:
#         STATS.log['broke'].append(datetime.datetime.now())
#     STATS.writeTimestamps()
#     # print(log)
#     STATS.getStats()
#     return redirect(url_for('status'))


@app.route("/api/login", methods=["POST"])
def login():
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
            return jsonify(data)
        elif result == 0:
            data = {"mailSuccess": False, "loginSuccess": False}
            return jsonify(data)
        elif result == -1:
            data = {"mailSuccess": False, "loginSuccess": False}
            return jsonify(data)


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


@app.route("/api/creategame", methods=["POST"])
def createGame():
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


if __name__ == '__main__':
    # app.run(debug=False, host='42.0.139.255')
    app.run(debug=True, host='localhost')
