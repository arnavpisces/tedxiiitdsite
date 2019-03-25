import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
 


def sendemail(data):
	count=0

	for det in data:
		count+=1
		imagename=""
		# if(count==2)
		fromaddr = "tedx@iiitd.ac.in"
		cc = "shubhang16198@iiitd.ac.in"
		toaddr = det[1]
		print(det)
		# toaddr = "arnav16017@iiitd.ac.in"
		names = det[0].split(" ")
		if(len(names)==2):
			firstname, lastname = names[0], names[1]
		else:
			firstname= names[0]
		filename="./tickets/new/"
		imagename=firstname+"_"+str(det[2])+"_"+str(count)+".jpg"
		finalname=filename+imagename
		# if(firstname=="Shagun"):
			# print("ha")
			# cc+=",royal17310@iiitd.ac.in"
		# print(firstname)
		# print("sadjfsadjfd")
		# toaddr = data["buyer"]
		# toaddr=data[det[1]]
		rcpt = cc.split(",") + [toaddr]
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Cc'] = cc
		msg['Subject'] = "Your Ticket to TEDxIIITD"
		
		body = "<span style='font-family: arial; font-size: 20px;'>Hi!<br><br>Just a gentle reminder that the entry will start at 2pm and the venue is <a href=\"https://www.google.com/maps/place/28%C2%B032'43.2%22N+77%C2%B016'23.2%22E/@28.5453409,77.2722404,18z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!7e2!8m2!3d28.5453395!4d77.2731086\" style=\"color: black; font-weight: bolder;\">Seminar Block, IIIT-Delhi</a><br><br>Hoping to see you soon<br><br>Look out for The Smaller Picture!<br>Team TEDxIIITD</span>"
		msg.attach(MIMEText(body, 'html'))

		# filepath = "tickets/" + filename
		# attachment = open(finalname)
		# part = MIMEBase('application', 'octet-stream')
		# part.set_payload((attachment).read())
		# encoders.encode_base64(part)
		# part.add_header('Content-Disposition', "attachment; filename= %s" % imagename)
		# msg.attach(part)

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "march18/19")
		text = msg.as_string()
		server.sendmail(fromaddr, rcpt, text)
		server.quit()
		# if(count==1):
			# return

if __name__=='__main__':
	sendemail(["a b","a",600])