from sqlalchemy import null
from myapp import myapp_obj
from myapp.forms import LoginForm, SignupForm, EditProfile, AgencySignupForm, ListingForm, VolunteerForm, NewName, NewDesc, NewPrice, ReviewForm, ReportForm, Adddonations, EditPicture, ChangePassword, SearchForm, SendMessageForm, SendMsgForm, ProfileMessage, SearchMessageForm
from flask import render_template, flash, redirect
from flask import Flask, url_for
from sqlalchemy import and_, or_, not_

from myapp import db
from myapp.models import User, Profile, Listing, Volunteer, BeVolunteer, Rating, Report, AddDonations, Review, Messages
from flask_login import current_user, login_user, logout_user, login_required
import stripe
import os


@myapp_obj.route("/")
def home():

	return render_template('home.html')

"""




SIGN UP




"""

@ myapp_obj.route("/signup", methods=['GET', 'POST'])
def signup():
    """
    This function returns the signup page with the SignUpForm

    Parameters:
    ----------
        none
    Return:
    ------
        redirects to login.html
    """
    form = SignupForm()
    if form.validate_on_submit():
        flash(f'Welcome!')
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username, email)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template('signup.html', form=form)

@ myapp_obj.route("/agencysignup", methods=['GET', 'POST'])
def agencysignup():
    """
    This function returns the signup page with the SignUpForm

    Parameters:
    ----------
        none
    Return:
    ------
        redirects to login.html
    """
    form = AgencySignupForm()
    if form.validate_on_submit():
        flash(f'Welcome!')
        username = form.username.data
        email = form.email.data
        password = form.password.data
        agency = 'True'
        verified = 'False'
        user = User(username, email)
        user.set_password(form.password.data)
        user.set_agency(agency)
        user.set_verified(verified)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template('agencysignup.html', form=form)


"""



LOGIN / LOGOUT



"""

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Incorrect username or password!', 'error')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        if user.agency == 'True':
            return redirect('/agencyprofile')
        if user.admin == 'True':
            return redirect('/adminprofile')
        else:
            return redirect('/profile')
    return render_template('login.html', form = form)


@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('home.html')


"""



PROFILES




"""

@myapp_obj.route("/profile")
@login_required
def profile():
    username = current_user.username
    user_id = current_user.id
    agency = current_user.agency
    admin = current_user.admin
    if agency == 'True':
        return redirect('/agencyprofile')
    if admin == 'True':
        return redirect('/adminprofile')
    a = Review.query.filter(Review.user_id==current_user.id).all()
    rating = Rating.query.filter(Rating.user_id==current_user.id).first()
    listings = Listing.query.filter(Listing.user_id==current_user.id)

    count = Listing.query.filter(Listing.user_id==user_id).count()
    sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
    return render_template('profile.html', username = username, agency=agency, listings=listings, count=count, sold=sold, user=current_user, a=a, rating=rating)

@myapp_obj.route("/changepassword", methods=['GET', 'POST'])
@login_required
def changepassword():
	user_id = current_user.id
	user = User.query.get(user_id)
	username = user.username
	a = Review.query.filter(Review.user_id==current_user.id).all()
	rating = Rating.query.filter(user_id==current_user.id).first()
	listings = Listing.query.filter(Listing.user_id==user_id)
	count = Listing.query.filter(Listing.user_id==user_id).count()
	sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
	form = ChangePassword()
	if form.validate_on_submit():
		user = User.query.filter(User.id == user_id).first()
		if user is not user.check_password(form.password.data):
			print(form.password.data)
			flash('Incorrect username or password!', 'error')
			return redirect('/login')
		user.set_password(form.newpassword.data)
		db.session.commit()
		return redirect('/profile')
	return render_template('changepassword.html',username = username, listings=listings, count=count, sold=sold, user=current_user, a=a, rating=rating, form=form )




@myapp_obj.route("/agencyprofile")
@login_required
def agencyprofile():
    username = current_user.username
    user = current_user
    user_id = current_user.id
    listings = Volunteer.query.filter(Volunteer.user_id==user_id)
    return render_template('agencyprofile.html', username = username, listings=listings, user=user)

def profile_image(profile_file):
    pic_name = profile_file.filename
    picture_path = os.path.join(myapp_obj.root_path, 'static/profile_pics', pic_name)
    profile_file.save(picture_path)
    return pic_name

@myapp_obj.route("/editprofile", methods=['GET', 'POST'])
@login_required
def edit():
    username = current_user.username
    user_id = current_user.id
    user = User.query.get(user_id)

    form = EditProfile()
    if form.validate_on_submit():
        flash(f'Changes Saved')
        user = User.query.get(current_user.id)
        first = form.first.data
        last = form.last.data
        phone = form.phone.data
        address1 = form.address1.data
        address2 = form.address2.data
        postal = form.postal.data
        state = form.state.data
        user_id = current_user.id
        profile = Profile.query.get(user.id)
        print(profile)
        if profile is None:
            prof = Profile(first, last, phone, address1, address2, postal, state, user_id)
            db.session.add(prof)
        else:
            profile.set_first(first)
            profile.set_last(last)
            profile.set_phone(phone)
            profile.set_address1(address1)
            profile.set_address2(address2)
            profile.set_postal(postal)
            profile.set_state(state)


        db.session.commit()
        return redirect('/profile')
    image_url = url_for('static', filename='profile_pics/' + current_user.image_file)
    profile = Profile.query.get(user_id)
    return render_template('editprofile.html', user=user, form=form, username=username, profile=profile, image_url = image_url)

@myapp_obj.route('/editpic', methods=['GET', 'POST'])
@login_required
def editpic():
	user_id = current_user.id
	user = User.query.get(user_id)
	username = current_user.username
	form = EditPicture()
	a = Review.query.filter(Review.user_id==current_user.id).all()
	rating = Rating.query.filter(user_id==current_user.id).first()
	listings = Listing.query.filter(Listing.user_id==user_id)
	count = Listing.query.filter(Listing.user_id==user_id).count()
	sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
	if form.validate_on_submit():
		image_file = profile_image(form.picture.data)
		user.set_image_file(image_file)
		print(user.image_file)
		db.session.commit()
		return redirect('/profile')
	return render_template("editpic.html",username = username, listings=listings, count=count, sold=sold, user=current_user, a=a, rating=rating, form=form)

@myapp_obj.route('/adminprofile')
@login_required
def adminprofile():
    fraud = Report.query.all()
    apps = AddDonations.query.all()
    count = Report.query.count()
    count2 = AddDonations.query.count()
    return render_template('adminprofile.html', fraud=fraud, apps=apps, count=count, count2=count2 )

@myapp_obj.route('/viewprofile/<int:val>')
def viewProfile(val):
    user_id = val
    user = User.query.get(val)
    print(user)
    listings = Listing.query.filter(Listing.user_id==user_id)
    rating = Rating.query.filter(Rating.user_id==val).first()
    a = Review.query.filter(Review.user_id==val).all()
    count = Listing.query.filter(Listing.user_id==user_id).count()
    sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
    return render_template('viewprofile.html', rating=rating, user=user, count=count, sold=sold, listings=listings, a=a)


"""



CREATE AND LIST ITEMS



"""

from myapp import myapp_obj
from myapp.forms import LoginForm, SignupForm, EditProfile, AgencySignupForm, ListingForm, VolunteerForm
from flask import render_template, flash, redirect, url_for
from flask import Flask

from myapp import db
from myapp.models import User, Profile, Listing, Volunteer
from flask_login import current_user, login_user, logout_user, login_required


def save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(myapp_obj.root_path, 'static/listing_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name

@myapp_obj.route("/createlisting", methods=['GET', 'POST'])
@login_required
def itemsForSale():
    form = ListingForm()
    user_id = current_user.id
    # a = User.query.with_entities(User.agency == 'True').all()
    a = User.query.filter(User.verified =='True').all()
    # form.agency.choices = [('0', 'None')] + a

    form.agency.choices = a
    a.insert(0,None)
	# form.agency.default = [('0', '-- select an option --')]


    if form.validate_on_submit():
        flash(f'Created!')
        name = form.name.data
        description = form.description.data
        location = int(form.location.data)
        agency = form.agency.data
        warehouse = form.warehouse.data
        free = form.free.data
        trade = form.trade.data
        image_file = save_image(form.picture.data)
        Listing.image_file = image_file
        listing = Listing(image_file, name, description, location, agency, warehouse, free, trade, user_id)
        if free is True:
            listing.set_price(0.00)
        elif trade is True:
            listing.set_price(0.00)
        else:
            listing.set_price(form.price.data)
        db.session.add(listing)
        db.session.commit()
        return redirect('/managelistings/'+ str(listing.id))
    # else:
    #     return redirect('/createerror')
    image_url = url_for('static', filename='listing_pics/'+ Listing.image_file)
    return render_template('listitem.html', a=a, form=form, image_url = image_url)

@myapp_obj.route("/createerror")
@login_required
def createerror():
	form = ListingForm()
	return render_template('createerror.html', form=form)

@myapp_obj.route("/createditem")
@login_required
def itemTest():
	item = Listing.query.get(listing_id)
	user_id = current_user.id
	user = User.query.get(user_id)
    # form = Listing.query.all()
	return render_template('testfile.html', item=item, user=user)

# @myapp_obj.route('/freelistings')
# @login_required
# def freelistings():
#     sale = Listing.query.filter(Listing.free==True)
#     title = "Free Listings"
#     return render_template('listings.html', sale=sale, title=title)
#
# @myapp_obj.route('/tradelistings')
# @login_required
# def tradelistings():
#     sale = Listing.query.filter(Listing.trade==True)
#     title = "Trade Listings"
#     return render_template('listings.html', sale=sale, title=title)
#
#
# @myapp_obj.route('/listings')
# @login_required
# def listings():
#     sale = Listing.query.filter(Listing.free==False, Listing.trade==False)
#     title = "Sale Listings"
#     return render_template('listings.html', sale=sale, title=title)

@myapp_obj.route('/listings/<int:val>')
@login_required
def getListing(val):
    listing_id = val
    item = Listing.query.get(listing_id)
    user = User.query.get(item.user_id)
    items = []
    return render_template('testfile.html', items=items, item=item, user=user)

@myapp_obj.route('/freelistings/<int:val>')
@login_required
def free(val):
    listing_id = val
    item = Listing.query.get(listing_id)
    items = []
    user_id = current_user.id
    user = User.query.get(user_id)
    return render_template('freeitem.html', items=items, item=item, user=user)

@myapp_obj.route('/tradelistings/<int:val>')
@login_required
def trade(val):
    listing_id = val
    item = Listing.query.get(listing_id)
    items = []
    user_id = current_user.id
    user = User.query.get(user_id)
    return render_template('tradeitem.html', items=items, item=item, user=user)

@myapp_obj.route('/getitfree/<int:val>')
@login_required
def getitfree(val):
    listing_id = val
    user_id = current_user.id
    listings = Listing.query.filter(Listing.user_id==user_id)
    count = Listing.query.filter(Listing.user_id==user_id).count()
    sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()

    item = Listing.query.get(listing_id)
    items = []
    user = User.query.get(user_id)
    item.status="Sold"
    db.session.commit()
    a = Review.query.filter(Review.user_id==current_user.id).all()
    rating = Rating.query.filter(Rating.user_id==current_user.id).first()

    return render_template('getitfree.html', items=items, item=item, count=count, sold=sold, listings= listings, user=user, rating=rating)

@myapp_obj.route('/bought/<int:val>')
@login_required
def bought(val):
	listing_id = val
	item = Listing.query.get(listing_id)
	name = item.name
	item.status="Sold"
	db.session.commit()
	return redirect(url_for('success', name=name))
	# return render_template('testfile.html', items=items, item=item)

@myapp_obj.route('/success/<string:name>')
@login_required
def success(name):
	user_id = current_user.id
	user = current_user
	listings = Listing.query.filter(Listing.user_id==user_id)
	count = Listing.query.filter(Listing.user_id==user_id).count()
	sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
	rating = Rating.query.filter(user_id==current_user.id).first()
	a = Review.query.filter(Review.user_id==current_user.id).all()
	return render_template('success.html', name=name, listings=listings, sold=sold, count=count, rating=rating, a=a, user=user)


@myapp_obj.route('/managelistings/<int:val>')
@login_required
def manageListing(val):
    listing_id = val
    item = Listing.query.get(listing_id)

    return render_template('managelisting.html',  item=item)


@myapp_obj.route('/newname/<int:val>', methods=['GET', 'POST'])
def newName(val):
	item = Listing.query.get(val)
	form = NewName()
	value=val
	if form.validate_on_submit():
		flash(f'Changes Saved!')
		newname = form.name.data
		item.name = newname

        # db.session.query(Listing).filter(
        # Listing.id == val).update({Listing.name: name})
		db.session.commit()
		return redirect(url_for('manageListing', val=value))
	return render_template('newname.html', form=form, item=item, val=val)

@myapp_obj.route('/newdesc/<int:val>', methods=['GET', 'POST'])
def newDesc(val):
	item = Listing.query.get(val)
	form = NewDesc()
	value=val
	if form.validate_on_submit():
		flash(f'Changes Saved!')
		newdesc = form.desc.data
		item.description = newdesc

        # db.session.query(Listing).filter(
        # Listing.id == val).update({Listing.name: name})
		db.session.commit()
		return redirect(url_for('manageListing', val=value))
	return render_template('newdesc.html', form=form, item=item, val=val)

@myapp_obj.route('/newprice/<int:val>', methods=['GET', 'POST'])
def newPrice(val):
	item = Listing.query.get(val)
	form = NewPrice()
	value=val
	if form.validate_on_submit():
		flash(f'Changes Saved!')
		newprice = form.price.data
		item.price = newprice
		if item.free is True:
			item.free = False

        # db.session.query(Listing).filter(
        # Listing.id == val).update({Listing.name: name})
		db.session.commit()
		return redirect(url_for('manageListing', val=value))
	return render_template('newprice.html', form=form, item=item, val=val)

@myapp_obj.route('/delete/<int:val>')
def deleteItem(val):
	item = Listing.query.get(val)
	db.session.delete(item)
	db.session.commit()
	return redirect('/profile')

@myapp_obj.route('/deletevol/<int:val>')
def deletevol(val):
	item = Volunteer.query.get(val)
	db.session.delete(item)
	db.session.commit()
	return redirect('/profile')
"""



VOLUNTEER




"""

@myapp_obj.route('/listvolunteer', methods=['GET', 'POST'])
@login_required
def listvolunteer():
    user_id = current_user.id
    form = VolunteerForm()
    if form.validate_on_submit():
        flash(f'Created!')
        name = form.name.data
        description = form.description.data
        location = form.location.data
        date = form.date.data
        image_file = save_image(form.picture.data)
        Volunteer.image_file = image_file
        vol = Volunteer(image_file, name, description, location, date, user_id)
        db.session.add(vol)
        db.session.commit()
        return redirect('/managevol/'+ str(vol.id))
    return render_template('listvolunteer.html', form=form)

@myapp_obj.route("/createdvol")
@login_required
def volTest():
    items = Volunteer.query.all()
    user_id = current_user.id
    user = User.query.get(user_id)
    return render_template('testfile.html', items=items, user=user)

# @myapp_obj.route('/vollisting')
# @login_required
# def vollistings():
#     sale = Volunteer.query.all()
#     title = "Volunteer Opportunities"
#     return render_template('getvol.html', sale=sale, title=title)

@myapp_obj.route('/deletevol/<int:val>')
def deleteVol(val):
	item = Volunteer.query.get(val)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('listings'))

@myapp_obj.route('/volsuccess/<int:val>')
def volsuccess(val):
    vol = Volunteer.query.get(val)
    return render_template('volsuccess.html', item=vol)



@myapp_obj.route('/volunteer')
@login_required
def volunteer():
    return render_template('VolunteerList.html')

@myapp_obj.route('/vollistings/<int:val>')
@login_required
def volListings(val):
    listing_id = val
    item = Volunteer.query.get(listing_id)
    items = []
    return render_template('vollistings.html', items=items, item=item)

@myapp_obj.route("/adddonations", methods=['GET', 'POST'])
@login_required
def adddonations():
    user_id = current_user.id
    username = current_user.username

    listings = Volunteer.query.filter(Volunteer.user_id==user_id)
    form = Adddonations()
    if form.validate_on_submit():
        flash("Successfully")
        name = current_user.username
        email = current_user.email
        phone = form.phone.data
        account = form.account.data
        date = form.date.data
        user_id = current_user.id
        application = AddDonations(name, phone, email, account, date, user_id)
        db.session.add(application)
        db.session.commit()

        return redirect(url_for('agencyprofile', username=username, user_id=user_id, listings=listings, user=current_user))
    return render_template('adddonations.html', form=form, username=username, user_id=user_id, listings=listings, user=current_user)

@myapp_obj.route('/bevolunteer/<int:val>', methods=['GET', 'POST'])
@login_required
def bevolunteer(val):
    user = current_user.id
    print(user)
    vol_id = val
    bevol = BeVolunteer(user, vol_id)
    db.session.add(bevol)
    db.session.commit()
    # return redirect('/volsuccess')
    return redirect(url_for('volsuccess', val=val))

@myapp_obj.route('/managevol/<int:val>')
@login_required
def manageVol(val):
    listing_id = val
    item = Volunteer.query.get(listing_id)
    vols = BeVolunteer.query.filter(BeVolunteer.vol_id == listing_id).all()
    print(vols)
    a = []
    for i in vols:
        us = get_username(i.user_id)
        print(us)
        a.append(us)

    # for c,i in db.session.query(User, BeVolunteer).filter(User.bevolunteer == vols.user_id):
    #     user = get_username(c.id)
    #     a.append(c.get_username())

    return render_template('managevol.html',  item=item, vols=vols, a=a)

def get_username(user_id):
    user_id = user_id
    user = User.query.get(user_id)
    return user

@myapp_obj.route('/volname/<int:val>', methods=['GET', 'POST'])
def volName(val):
	item = Volunteer.query.get(val)
	form = NewName()
	value=val
	vols = BeVolunteer.query.filter(BeVolunteer.vol_id == val).all()
	a = []
	for i in vols:
		us = get_username(i.user_id)
		a.append(us)
	if form.validate_on_submit():
		flash(f'Changes Saved!')
		newname = form.name.data
		item.name = newname

        # db.session.query(Listing).filter(
        # Listing.id == val).update({Listing.name: name})
		db.session.commit()
		return redirect(url_for('manageVol', val=value, item=item, vols=vols, a=a))
	return render_template('volname.html', form=form, item=item, val=val)

@myapp_obj.route('/voldesc/<int:val>', methods=['GET', 'POST'])
def volDesc(val):
	item = Volunteer.query.get(val)
	form = NewDesc()
	value=val
	vols = BeVolunteer.query.filter(BeVolunteer.vol_id == val).all()
	a = []
	for i in vols:
		us = get_username(i.user_id)
		a.append(us)
	if form.validate_on_submit():
		flash(f'Changes Saved!')
		newdesc = form.desc.data
		item.description = newdesc

        # db.session.query(Listing).filter(
        # Listing.id == val).update({Listing.name: name})
		db.session.commit()
		return redirect(url_for('manageVol', val=value, item=item, vols=vols, a=a))
	return render_template('voldesc.html', form=form, item=item, val=val)
"""



PAYMENTS



"""

YOUR_DOMAIN = 'http://127.0.0.1:5000'
stripe.api_key = 'sk_test_51KwJCGIVxGuZvYFf0YW5nfbMrKiW4fmwQZfpuOM1ai8b1y1CZb5OXKIFxbfGNhzW4DebQE2g7RC6ABu6Xq9NIC9D00eYLOFkSj'

@myapp_obj.route('/purchase/<int:val>', methods=['GET','POST'])
def create_checkout_session(val):
    item_id = val
    item = Listing.query.get(item_id)
    integer_price = int(item.price * 100)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                  'price_data': {
                    'currency': 'usd',
                    'product_data': {
                      'name': item.name,
                    },
                    'unit_amount': integer_price,
                  },
                  'quantity': 1,
                }],
                mode='payment',
                success_url=YOUR_DOMAIN+ '/bought/'+str(val),
                cancel_url=YOUR_DOMAIN+ '/listings/'+str(val),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)



"""



REPORT USERS



"""

@myapp_obj.route('/report/<int:val>', methods=['GET','POST'])
def report(val):
    user_id = val
    form = ReportForm()
    listings = Listing.query.filter(Listing.user_id==user_id)
    count = Listing.query.filter(Listing.user_id==user_id).count()
    sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
    rating = Rating.query.filter(Rating.user_id==val).first()
    a = Review.query.filter(Review.user_id==val).all()
    user = User.query.get(val)
    if form.validate_on_submit():
        reason= form.reason.data
        user_id = val
        name = user.username
        report = Report(user_id, reason, name)
        db.session.add(report)
        db.session.commit()

        return redirect(url_for('viewProfile', val=val, listings=listings, sold=sold, count=count, user=user, rating=rating, a=a))


    return render_template('report.html', val=val, form=form, user=user, count=count, sold=sold, listings=listings, rating=rating, a=a)


@myapp_obj.route('/report/deleteuser/<int:val>/<int:rep>')
@login_required
def foundFraud(val, rep):
	user = User.query.get(val)
	report = Report.query.get(rep)
	apps = AddDonations.query.all()
	count2 = AddDonations.query.count()
	listings = Listing.query.filter(Listing.user_id == val).all()
	for i in listings:
		db.session.delete(i)
	db.session.delete(user)
	db.session.delete(report)
	db.session.commit()
	fraud = Report.query.all()
	count = Report.query.count()
	return redirect(url_for('adminprofile', fraud=fraud, apps=apps, count=count, count2=count2))

@myapp_obj.route('/report/deletereport/<int:val>')
@login_required
def delReport(val):
	report = Report.query.get(val)
	db.session.delete(report)
	db.session.commit()
	fraud = Report.query.all()
	count = Report.query.count()
	apps = AddDonations.query.all()
	count2 = AddDonations.query.count()
	return redirect(url_for('adminprofile', fraud=fraud, apps=apps, count=count, count2=count2))


@myapp_obj.route('/approve/<int:val>/<int:appl>')
@login_required
def approve(val, appl):
	user = User.query.get(val)
	verified = "True"
	user.set_verified(verified)
	appl = AddDonations.query.get(appl)
	db.session.delete(appl)
	db.session.commit()
	fraud = Report.query.all()
	count = Report.query.count()
	apps = AddDonations.query.all()
	count2 = AddDonations.query.count()
	return redirect(url_for('adminprofile', fraud=fraud, apps=apps, count=count, count2=count2))

@myapp_obj.route('/deny/<int:val>')
@login_required
def deny(val):
	application = AddDonations.query.get(val)
	db.session.delete(application)
	db.session.commit()
	fraud = Report.query.all()
	count = Report.query.count()
	apps = AddDonations.query.all()
	count2 = AddDonations.query.count()
	return redirect(url_for('adminprofile', fraud=fraud, apps=apps, count=count, count2=count2))


"""



REVIEW:


"""

@myapp_obj.route('/reviewthis/<int:val>', methods=['GET','POST'])
def review(val):
	listings = Listing.query.filter(Listing.user_id==val)
	user_id = val
	name = current_user.username
	count = Listing.query.filter(Listing.user_id==val).count()

	sold = Listing.query.filter(Listing.user_id==val and Listing.status=='Sold').count()
	form = ReviewForm()
	user = User.query.get(val)
	b = Rating.query.filter(Rating.user_id == val).all()
	rat = 0
	for i in b:
		rat = i.rating
		item = i
	if form.validate_on_submit():
		rating = int(form.rating.data)
		temp = rating
		review = form.review.data
		if rat > 0:
			rating = (rat + rating)/2
			item.set_rating(rating)
			rev = Review(review, temp, name, user_id)
			db.session.add(rev)
		else:
			ratin = Rating(rating, user_id)
			db.session.add(ratin)
			rev = Review(review, temp, name, user_id)
			db.session.add(rev)


		db.session.commit()
		rating = Rating.query.filter(Rating.user_id==val).first()
		a = Review.query.filter(Review.user_id==val).all()
		return redirect(url_for('viewProfile', val=val, user=user, count=count, sold=sold, listings=listings, rating=rating, a=a))

	rating = Rating.query.filter(Rating.user_id==val).first()
	a = Review.query.filter(Review.user_id==val).all()
	return render_template('review.html', form=form, user=user, count=count, sold=sold, listings=listings, rating=rating, a=a)


@myapp_obj.route('/listings', methods=['GET','POST'])
def search():
	sale = Listing.query.filter(Listing.free==False, Listing.trade==False)
	title = "Sale Listings"
	count = Listing.query.filter(Listing.status == 'For Sale', Listing.free==False, Listing.trade==False).count()

	form = SearchForm()
	ret = []
	good = False
	print(form.search.data)
	search = form.search.data
	print(search)
	if search is not None:
		words = search.split(" ")
		for word in words:
			name = Listing.query.filter(Listing.free==False, Listing.trade==False, Listing.name.contains(word)).all()

			if len(name) == 0:
				print(len(name))
				desc = Listing.query.filter(Listing.free==False, Listing.trade==False, Listing.description.contains(word)).all()
				name.extend(desc)
			print(name)
			ret = name
			res = []
			for i in ret:
				if i not in res:
					res.append(i)
			sale = res
			good = True
			print(sale)

			if len(sale) == 0:
				count = 0


		return render_template('listings.html', sale=sale, title=title, form=form, count=count, good=good)

	return render_template('listings.html', sale=sale, title=title, form=form, count=count, good=good)

@myapp_obj.route('/freelistings', methods=['GET','POST'])
def freesearch():
	sale = Listing.query.filter(Listing.status=='For Sale', Listing.free==True)
	title = "Free Listings"
	count = Listing.query.filter(Listing.status == 'For Sale', Listing.free==True).count()
	good = False
	form = SearchForm()
	ret = []
	print(form.search.data)
	search = form.search.data
	print(search)
	if search is not None:
		words = search.split(" ")
		for word in words:
			name = Listing.query.filter(Listing.free==True, Listing.name.contains(word)).all()

			if len(name) == 0:
				print(len(name))
				desc = Listing.query.filter(Listing.free==True, Listing.description.contains(word)).all()
				name.extend(desc)
			print(name)
			ret = name
			res = []
			for i in ret:
				if i not in res:
					res.append(i)
			sale = res
			good = True
			print(sale)

			if len(sale) == 0:
				count = 0



		return render_template('listings.html', sale=sale, title=title, form=form, count=count, good=good)

	return render_template('listings.html', sale=sale, title=title, form=form, count=count, good=good)

@myapp_obj.route('/tradelistings', methods=['GET','POST'])
def tradesearch():
	sale = Listing.query.filter(Listing.trade==True)
	title = "Trade Listings"
	count = Listing.query.filter(Listing.trade==True).count()
	good = False

	form = SearchForm()
	ret = []
	print(form.search.data)
	search = form.search.data
	print(search)
	if search is not None:
		words = search.split(" ")
		for word in words:
			names = Listing.query.filter(Listing.trade==True).all()


			name = Listing.query.filter(Listing.trade==True, Listing.name.contains(word)).all()

			if len(name) == 0:
				print(len(name))
				desc = Listing.query.filter(Listing.trade==True, Listing.description.contains(word)).all()
				name.extend(desc)
			print(name)
			ret = name
			res = []
			for i in ret:
				if i not in res:
					res.append(i)
			sale = res
			good = True
			print(sale)

			if len(sale) == 0:
				count = 0



		return render_template('listings.html', sale=sale, title=title, form=form, count=count, good=good)

	return render_template('listings.html', sale=sale, title=title, form=form, count=count, good=good)

@myapp_obj.route('/vollisting', methods=['GET','POST'])
def volsearch():
	sale = Volunteer.query.all()
	title = "Volunteer Opportunities"
	good = False

	count = Volunteer.query.count()

	form = SearchForm()
	ret = []
	print(form.search.data)
	search = form.search.data
	print(search)
	if search is not None:
		words = search.split(" ")
		for word in words:
			name = Volunteer.query.filter(Volunteer.name.contains(word)).all()

			if len(name) == 0:
				print(len(name))
				desc = Volunteer.query.filter(Volunteer.description.contains(word)).all()
				name.extend(desc)
			print(name)
			ret = name
			res = []
			for i in ret:
				if i not in res:
					res.append(i)
			sale = res
			print(sale)
			good = True

			if len(sale) == 0:
				count = 0



		return render_template('getvol.html', sale=sale, title=title, form=form, count=count, good=good)

	return render_template('getvol.html', sale=sale, title=title, form=form, count=count, good=good)

"""


MESSAGES


"""

@myapp_obj.route("/sendmessage", methods=['GET', 'POST'])
@login_required
def send_message():
    error = None
    form = SendMessageForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.sent_id.data).first()

        if user is None:
            error = 'Invalid username'
        else:
            send = User.query.filter(User.username==form.sent_id.data).first()
            message = Messages(user_id=current_user.username, user=current_user.id, content=form.content.data, sent_id=form.sent_id.data, send=send.id)
            db.session.add(message)
            db.session.commit()
            return redirect('/profile')
    return render_template('sendmessage.html', form=form, error=error)


@myapp_obj.route("/viewmessage", methods=['GET', 'POST'])
@login_required
def my_messages():
    messages = Messages.query.filter(or_(Messages.user_id==current_user.username,Messages.sent_id == current_user.username)).all()
    form = SearchMessageForm()
    user_id = None
    sent_id = None
    sent_id = form.search.data

    unreads = Messages.query.filter(and_(Messages.sent_id == current_user.username, Messages.message_viewed == False))
    if form.validate_on_submit():
        messages = Messages.query.filter(
            or_(and_(Messages.user_id == current_user.username, Messages.sent_id == sent_id),
                and_(Messages.user_id == sent_id, Messages.sent_id == current_user.username)
                )
            )
        receivedmessages = Messages.query.filter(and_(Messages.user_id == sent_id, Messages.sent_id == current_user.username))
        for receivedmessage in receivedmessages:
            receivedmessage.message_viewed = True
            db.session.commit()
        for message in messages:
            user_id = message.user_id
    return render_template('viewmessage.html', messages=messages, user_id=user_id, form = form, unreads=unreads)

@myapp_obj.route('/messagethis/<int:val>', methods=['GET','POST'])
def message(val):
    user_id = val
    form = ProfileMessage()
    listings = Listing.query.filter(Listing.user_id==user_id)
    count = Listing.query.filter(Listing.user_id==user_id).count()
    sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
    rating = Rating.query.filter(Rating.user_id==val).first()
    a = Review.query.filter(Review.user_id==val).all()
    user = User.query.get(val)
    if form.validate_on_submit():
        content= form.content.data
        user_id = val
        name = user.username
        sent = User.query.filter(User.username==name).first()
        message = Messages(user_id=current_user.username, user=current_user.id, content=content, sent_id=name, send=sent.id)
        db.session.add(message)
        db.session.commit()

        return redirect(url_for('viewProfile', val=val, listings=listings, sold=sold, count=count, user=user, rating=rating, a=a))


    return render_template('message.html', val=val, form=form, user=user, count=count, sold=sold, listings=listings, rating=rating, a=a)
