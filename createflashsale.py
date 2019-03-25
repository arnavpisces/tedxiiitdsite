from app import Ticket, db
import sys


numberoftickets = int(sys.argv[1])

for i in range(numberoftickets):
	tick = Ticket("", 0, "")
	db.session.add(tick)

db.session.commit()