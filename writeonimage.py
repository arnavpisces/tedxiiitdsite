from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from mailer import sendemail

def WriteOnImage(data):
	count=0
	for det in data:
		count=91
		# if(count==50):
			# return
		#det[0] is the name, det[1] is the email id, det[2] is the price of the ticket
		img="./tickets/"
		print(det)
		if(int(det[2])==int(600)):
			img+=str(det[2])
			img+=".jpg"
			# print(img)
		elif(int(det[2])==700):
			img+=str(det[2])
			img+=".jpg"
			# print(img)
		elif(int(det[2])==1000):
			img+=str(det[2])
			img+=".jpg"
			# print(img)
		elif(int(det[2])==1100):
			img+=str(det[2])		
			img+=".jpg"
			# print(img)
		# else:
		# 	# img+=str(det[2])		
		# 	img+="test.jpg"
		# 	print(img)
		# return
		# img = Image.open("./tickets/1100.jpg")
		imgo = Image.open(img)
		imgo.show()
		draw = ImageDraw.Draw(imgo)
		font = ImageFont.truetype("./static/olivia.otf", 45)
	# name = data["buyer_name"]
		# name=det[0].split(" ")
		# name="blahblha blahhsadflksadjf"
		names = det[0].split(" ")
		if(len(names)==2):
			firstname, lastname = names[0], names[1]
			toprint = firstname + "\n" + lastname
		else:
			firstname= names[0]
			toprint = firstname

		draw.text((1347, 152), toprint, (255, 255, 255), font=font)	
		filename="./tickets/new/"
		filename+=firstname+"_"+str(det[2])+"_"+str(count)+".jpg"
		print(filename)
		imgo.save(filename)
	sendemail(data)

if __name__ == "__main__":
	lis=["Shubham Gupta","shubham18055@iiitd.ac.in",600]
	abc=[]
	abc.append(lis)
	# abc.append(lis)
	WriteOnImage(abc)