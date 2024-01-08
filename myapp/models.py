from myapp import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Boolean
from flask_login import UserMixin
from myapp import login


class User(UserMixin, db.Model):
    """
        This class represent for User table in database

        Attributes:
        ----------
        id: int (primary key)
        username: string
        email: string
        password: string
        to_do: object (foreign key)
        activities: Object (foreign key)
        flaskcard: Object (foreign key)

        Function:
        ---------
        __init__: constructor with 2 parameter username, email
        __repr__: representation a output
        set_password: auto generate password
        check_password: get and check password
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    image_file = db.Column(db.String(20),nullable=False,default='person.jpeg')
    admin = db.Column(db.String(10))
    agency = db.Column(db.String(10))
    verified = db.Column(db.String(10))
    profile = db.relationship('Profile', backref='users', lazy='dynamic')
    listings = db.relationship('Listing', backref='users', lazy='dynamic')
    volunteer = db.relationship('Volunteer', backref='users', lazy='dynamic')
    bevolunteer = db.relationship('BeVolunteer', backref='users', lazy='dynamic')
    report = db.relationship('Report', backref='users', lazy='dynamic')
    review = db.relationship('Review', backref='users', lazy='dynamic')
    rating = db.relationship('Rating', backref='users', lazy='dynamic')

    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email

    def __init__(self, username, email):
        self.username = username
        self.email = email


    def __repr__(self):
        return f'{self.username}'

    def set_time_login(self, timelogin):
        self.timelogin = timelogin

    def set_time_logout(self, timeloguot):
        self.timelogin = timeloguot

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def set_agency(self, agency):
        self.agency = agency

    def set_verified(self, verified):
        self.verified = verified

    def set_admin(self, admin):
        self.admin = admin

    def set_rating(self, rating):
        self.rating = ratings

    def set_review(self, review):
        self.review = review

    def set_image_file(self, image_file):
        self.image_file = image_file

    def check_password(self, password):
        return check_password_hash(self.password, password)





@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key = True)
    first = db.Column(db.String(64))
    last = db.Column(db.String(64))

    phone = db.Column(db.String(64))
    address1 = db.Column(db.String(128))
    address2 = db.Column(db.String(128))
    postal = db.Column(db.Integer)
    state = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self , first, last, phone, address1, address2, postal, state, user_id):
        self.first = first
        self.last = last
        self.phone = phone
        self.address1 = address1
        self.address2 = address2
        self.postal = postal
        self.state = state
        self.user_id = user_id

    def set_first(self, first):
        self.first = first

    def set_last(self, last):
        self.last = last

    def set_phone(self, phone):
        self.phone = phone

    def set_address1(self, address1):
        self.address1 = address1

    def set_address2(self, address2):
        self.address2 = address2

    def set_postal(self, postal):
        self.postal = postal

    def set_state(self, state):
        self.state = state

# class Rating(db.Model):
#     __tablename__ = 'ratings'
#     id = db.Column(db.Integer, primary_key = True)
#     rating = db.Column(db.Float)
#     user_id


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    name = db.Column(db.String(64))
    description = db.Column(db.String(512))
    location = db.Column(db.Integer)
    agency = db.Column(db.String(128))
    warehouse = db.Column(db.Boolean, default=False)
    free = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, default=0.00)
    trade = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String, default='For Sale')

    def __init__(self, image_file, name, description, location, agency, warehouse, free, trade, user_id):
        self.image_file = image_file
        self.name = name
        self.description = description
        self.location = location
        self.agency = agency
        self.warehouse = warehouse
        self.free = free
        self.trade = trade
        self.user_id = user_id

    def set_price(self, price):
        self.price = price

    def set_name(self, name):
        self.name = name

    def set_desc(self, description):
        self.description = description

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    name = db.Column(db.String(64))
    description = db.Column(db.String(512))
    location = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vol_id = db.relationship('BeVolunteer', backref='volunteer', lazy='dynamic')


    def __init__(self, image_file, name, description, location, date, user_id):
        self.image_file = image_file
        self.name = name
        self.description = description
        self.location = location
        self.date = date
        self.user_id = user_id

class AddDonations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(5))
    email = db.Column(db.String(512))
    account = db.Column(db.String(512))
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, phone,email, account, date, user_id):
        self.name = name
        self.phone = phone
        self.email = email
        self.account = account
        self.date = date
        self.user_id = user_id


class BeVolunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vol_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))

    def __init__(self, user_id, vol_id):
        self.user_id = user_id
        self.vol_id = vol_id

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float(3), default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, rating, user_id):
        self.rating = rating

        self.user_id = user_id

    def set_rating(self, rating):
        self.rating = rating

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    name = db.Column(db.String)
    review = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, review, rating, name, user_id):
        self.review = review
        self.rating = rating
        self.name = name
        self.user_id = user_id

class Report(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    username = db.Column(db.String)
    reason = db.Column(db.String(256))

    def __init__(self, user_id, reason, username):
        self.user_id = user_id
        self.reason = reason
        self.username = username

class Messages(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    send = db.Column(db.Integer)
    content = db.Column(db.String(128))
    user_id = db.Column(db.String(128))
    sent_id = db.Column(db.String(128))
    message_viewed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, content, user_id, user, sent_id, send):
        self.content = content
        self.user = user
        self.user_id = user_id
        self.sent_id = sent_id
        self.send = send
