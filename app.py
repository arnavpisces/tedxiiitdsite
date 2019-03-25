from flask import Flask, request, redirect, Response, render_template, session, url_for
from flask_login import LoginManager
from flask_login import (UserMixin, login_required, login_user, logout_user, current_user)
from flask_googlelogin import GoogleLogin
# from flask_oauth2_login import GoogleLogin
from flask_sqlalchemy import SQLAlchemy
from instamojo_wrapper import Instamojo
from writeonimage import WriteOnImage
from mailer import sendemail
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json

import hmac
import hashlib
import base64
import cStringIO
from datetime import datetime

SALESTATUS = 2

api = Instamojo(api_key="a401e463d7e1bb3581f5a4a77acc9d02", auth_token="63832165458b889a1cce5e850b17c542")


users = {}

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='static')
app.config.update(
    SECRET_KEY='SECRETSECRETKEY',
    GOOGLE_LOGIN_CLIENT_ID='207581121170-6ja4pfdp9ec09l2b3g0ufb9c2pk42k9o.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='Fahbsf_7hbKxnGUgaN3Z_s4x',
    GOOGLE_LOGIN_REDIRECT_URI='http://localhost:5000/oauth2callback',
    # GOOGLE_LOGIN_REDIRECT_URI='http://192.168.59.22:5000/oauth2callback',
    GOOGLE_LOGIN_SCOPES='https://www.googleapis.com/auth/userinfo.email')

googlelogin = GoogleLogin(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.sqlite3'
db = SQLAlchemy(app)


@app.route("/")
def index():
	return app.send_static_file('index.html')


@app.route("/speakers")
def speakers():
	return redirect("/#3")

@app.route("/pastspeakers")
def pastspeakers():
	return app.send_static_file('past.html')


@app.route("/partners")
def partners():
	return app.send_static_file('partners.html')

@app.route("/privacy")
def privacy():
	return app.send_static_file('privacy.html')

@app.route("/team")
def team():
	return app.send_static_file('team.html')


@app.route("/blog")
def blog():
	return app.send_static_file('blog.html')

@app.route("/nominate")
def nominate():
	return app.send_static_file('nominateaspeaker.html')

@app.route("/tickets")
def tickets():
	return app.send_static_file("buytickets.html")

@app.route("/underconstruction")
def underconstruction():
	return app.send_static_file('underconstruction.html')


@app.route("/flashsale")
def flashsale():
	return render_template("ffs.html", data=None)
	# return render_template("flashsale.html", data=None)

@app.route("/createticket/<name>/<email>")
def createticket(name, email):
	names = name.split(" ")
	firstname = names[0]
	lastname = ""
	for x in names[1:]:
		lastname += x + " "

	img = Image.open("./static/ticket.png")
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("./static/olivia.otf", 17)
	toprint = firstname + "\n" + lastname
	draw.text((510, 60), toprint, (255, 255, 255), font=font)
	filename = "offline_" + firstname + "_" + lastname + "_ticket.png"
	filepath = "./tickets/" + filename
	img.save(filepath)
	
	data = {"buyer" : email}
	sendemail(data, filename)
	return "E-mail sent to " + email



@app.route("/paymentresult")
def result():
	paymentid = request.args.get("payment_id")
	status = request.args.get("status")
	if paymentid == None:
		return redirect("/tickets")	

	if status == "failure":
		return render_template("thankyou.html", details={"status" : "failure"})

	response = api.payment_detail(paymentid)["payment"]

	return render_template("thankyou.html", details=response)

@app.route("/webhook", methods=['POST'])
# @app.route("/webh1ook", methods=['POST','GET'])
def webhook():
	# return "bitch9"
	# return Response(status=200)
	data = request.form
	mac = data['mac']
	print ("huheufe")
	datawithoutmac = {}
	for i in data:
		if i != "mac":
			datawithoutmac[i] = data[i]
	message = "|".join(v for k, v in sorted(datawithoutmac.items(), key=lambda x: x[0].lower()))
	mac_calculated = hmac.new("ce1a51c7f875438cbbfcd35ea5533128", message, hashlib.sha1).hexdigest()
	if mac == mac_calculated:
		if data['status'] == 'Credit':
			filename = data["buyer_name"].split(" ")[0] + "_" + data["payment_id"] + "_ticket.png"
			filepath = "tickets/" + filename
			WriteOnImage(data, filepath)
			sendemail(data, filename)

		else:
			#payment failed
			pass
			
		return Response(status=200)
	else:
		return Response(status=400)



def isIIIT(email):
	domain = email.split('@')[1]
	if domain == 'iiitd.ac.in':
		return True
	else:
		return False

class User(UserMixin):
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        self.picture = userinfo.get('picture')
        self.email = userinfo.get('email')


class Ticket(db.Model):
	id = db.Column('ticket_id', db.Integer, primary_key=True)
	allottee = db.Column(db.String(100))
	status = db.Column(db.Integer)
	timestamp = db.Column(db.String(100))


	def __init__(self, allottee, status, timestamp):
		self.allottee = allottee
		self.status = status
		self.timestamp = timestamp

@googlelogin.user_loader
def get_user(userid):
	return users.get(userid)

@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
	user = users[userinfo['id']] = User(userinfo)
	login_user(user)
	session['token'] = json.dumps(token)
	session['extra'] = params.get('extra')
	return redirect(params.get('next', url_for('flashsalelogin')))

@app.route('/logout')
def logout():
	logout_user()
	session.clear()
	return redirect("/flashsalelogin")

@app.route('/flashsalelogin')
@login_required
def flashsalelogin():
	if isIIIT(current_user.email):

		tickets = Ticket.query.all()
		# print(tickets)
		ticket = None
		response = ""
		status = None
		alreadyallotted = False
		WAITLIST_START_NO = 2

		if SALESTATUS == 0:
			status = "SALE_NOT_YET_STARTED"
			response = "The sale will start soon"

		else:
			for i in tickets:
				if i.allottee == current_user.email:
					alreadyallotted = True
					ticket = i
					break

			if not alreadyallotted:
				for i in tickets:
					if i.allottee == "":
						ticket = i
						break

			if ticket != None:
				if alreadyallotted:
					if Ticket.query.get(ticket.id).status == 1:
						status = "ALREADY_ALLOTTED"
						response = "Hey, you have already been allotted ticket no " + str(ticket.id)
					else:
						status = "ALREADY_ALLOTTED"
						response = "You have already been waitlisted"

				else:
					if ticket.id < WAITLIST_START_NO:
						status = "TICKET_AVAILABLE"
						response = "Ticket no. " + str(ticket.id) + " is available. Allotted!"
						Ticket.query.get(ticket.id).allottee = current_user.email
						Ticket.query.get(ticket.id).status = 1
						Ticket.query.get(ticket.id).timestamp = str(datetime.now())
						db.session.commit()

					else:
						status = "WAITLISTED"
						response = "You have been waitlisted!"
						Ticket.query.get(ticket.id).allottee = current_user.email
						Ticket.query.get(ticket.id).status = 0
						Ticket.query.get(ticket.id).timestamp = str(datetime.now())
						db.session.commit()

			else:
				status = "SALE_OVER"
				response = "You just missed it! The sale is over. Try again next time."

		data = {"status" : status, "message" : response}
		return render_template("ffs.html",  data=data)


	else:
		logout_user()
		session.clear()
		return "Not a IIITD account. Redirecting you to login page again... <img style='visibility:hidden;' src='https://mail.google.com/mail/u/0/?logout&hl=en' /><script>setTimeout(function(){window.location.href='/flashsalelogin';}, 1000)</script>"




if __name__ == "__main__":
	app.run(host='0.0.0.0')