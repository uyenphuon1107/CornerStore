from myapp.models import User
from myapp import db

def createadmin():
	name = 'admin1'
	password = 'Security'
	email = 'thisistheadmin1@cornerstore.com'
	admin = 'True'
	user = User(name, email)
	user.set_password(password)
	user.set_admin(admin)
	db.session.add(user)
	db.session.commit()
