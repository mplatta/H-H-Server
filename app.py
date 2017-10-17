from flask import Flask, request, render_template, redirect, url_for, flash
import datetime
import pickle
# from flask_restful import Resource, Api
# import sqlalchemy

app = Flask(__name__)
app.secret_key = 'some_secret'
#api = Api(app)

valid = False

class Stats:
	def __init__(self):
		self.path = 'timestamps'
		try:
			self.log = self.readTimestamps()
		except:
			self.log = {'repair':[], 'broke':[]}

	def readTimestamps(self):
		with open(self.path, 'rb') as f:
			log = pickle.load(f)
		return log

	def writeTimestamps(self):
		with open(self.path, 'wb') as f:
			pickle.dump(self.log, f)

	def getStats(self):
	
		def format(timedelta):
			table = str(timedelta).split(':')
			table=table[0].split(' ') + table[1:]
			string = table[0] + ' hours ' + table[1].replace('00','0') + ' minutes and ' + str(int(float(table[2]))) + ' seconds'
			return string

		global valid
		if len(self.log['repair']) > 0 and len(self.log['broke']) > 0:
			brokenTime = self.log['repair'][-1]-self.log['broke'][-1]
			validTime = self.log['broke'][-1]-self.log['repair'][-1]
			try:
				if self.log['highscore'] < validTime: 
					self.log['highscore'] = validTime
			except:
				self.log['highscore'] = validTime

			if valid:
				flash('Server was down for ' + format(brokenTime))
			else:
				flash('Server has stopped after ' + format(validTime) + ' of continous work.')
			flash(format(self.log['highscore']) + ' is actual record of server performence.')
		else:
			flash('Logs not found.')

STATS = Stats()

@app.route("/")
def status():
	global valid
	problems = ["Cannot connect to database"]
	return render_template("base.html", valid=valid, problems=problems)

@app.route('/api/msg/<id>', methods=['POST', 'GET'])
def serve(id):
	global valid
	if not valid:
		return redirect(url_for('status'))
	POOL = {'1':'Wiadomość pierwsza', '2':'Wiadomość druga', '2137':"Papież umarł", '992':"Ten numer to kłopoty!"}
	message = POOL[id]
	return render_template("message.html", valid=valid, message=message)

@app.route('/switch')
def switchValid():
	global valid
	global STATS
	valid = not valid
	if valid:
		STATS.log['repair'].append(datetime.datetime.now())
		flash('Successfully repaired server.')
	else:
		STATS.log['broke'].append(datetime.datetime.now())
	STATS.writeTimestamps()
	#print(log)
	STATS.getStats()
	return redirect(url_for('status'))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
	