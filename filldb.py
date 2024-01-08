import myapp
from myapp.models import User, Listing, Volunteer
from myapp import db
import datetime

from myapp import create_app, db
# Create the Flask app instance
app = create_app()

# Create an application context
with app.app_context():
    # Now you can safely use Flask-SQLAlchemy and other Flask extensions
    db.create_all()


user = User('admin','adminemail1@cornerstore.com')
user.set_password('Security1')
user.set_admin('True')
db.session.add(user)


agency = User('Default Agency','thisistheagency@cornerstore.com')
agency.set_password('password')
agency.set_agency('True')
agency.set_verified('True')
db.session.add(agency)


agency = User('Test Charity','thisisthecharity@cornerstore.com')
agency.set_password('password')
agency.set_agency('True')
agency.set_verified('False')
db.session.add(agency)

tester = User('Bob','thisistester@cornerstore.com')
tester.set_password('password')
db.session.add(tester)

tester1 = User('Alice','thisistester1@cornerstore.com')
tester1.set_password('password')
db.session.add(tester1)

listing1 = Listing('laptop.jpg', 'Mac Pro Laptop 2016', 'This laptop works but needs a new battery', '95125', 'None', False, False, False, 4)
listing1.set_price(145.45)
db.session.add(listing1)

listing2 = Listing('Grand-Piano.jpg', 'Grand Piano', "This piano was a gift but I don't have room for it", '95125', 'None', False, True, False, 4)
db.session.add(listing2)

listing3 = Listing('placeholder-image.png', 'Placeholder Card', "This is a placeholder card to use a a placeholder, I want to trade it for an actual picture", '95125', 'None', False, False, True, 4)
db.session.add(listing3)

listing4 = Listing('backpack.jpg', 'Osprey Backpack', "Osprey backpack 55L size women's small", '94087', 'None', False, False, False, 5)
listing4.set_price(98.00)
db.session.add(listing4)

listing5 = Listing('cookiecutters.jpg', 'Free Christmas Cookie Cutters', "Free cookie cutters from christmas last year.", '91234', 'None', False, True, False, 5)
db.session.add(listing5)

listing6 = Listing('guitar.png', 'Guitar', "Got this guitar as a gift but I can't figure out how to play it. Willing to trade it for another instrument or something of equal value.", '95125', 'None', False, False, True, 5)
db.session.add(listing6)

listing7 = Listing('hammock.jpg', 'Hammock for camping', "This is just the hammock, it doesn't have the straps to wrap around the tree", '95125', 'None', False, True, False, 5)
db.session.add(listing7)

listing8 = Listing('panda.jpg', 'Panda Squishmallow', "Never used. Great for kids", '12345', 'None', False, False, False, 4)
listing8.set_price(15.00)
db.session.add(listing8)

listing9 = Listing('tanjiro.jpg', 'Tanjiro Pop Doll', "Tanjiro from Demon Slayer Pop Doll, willing to trade for a different Demon Slayer pop", '91234', 'None', False, False, True, 5)
db.session.add(listing9)

listing10 = Listing('teacup.jpg', 'Cute Totoro Tea Cup', "This is a totoro cup that I won from a raffle but I just don't have space for it in my cupboard.", '91234', 'None', False, True, False, 4)
db.session.add(listing10)

date = datetime.datetime.now()
vol1 = Volunteer('beach.png', 'Beach Cleanup', 'Come join us for a beach cleanup on Saturday May 28th, 2022', '12345', date, 2)
db.session.add(vol1)
db.session.commit()
