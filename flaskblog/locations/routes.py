from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog.models import Location, Seat
from flaskblog import db
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog.locations.forms import LocationForm, SeatForm

locations = Blueprint('locations', __name__)

@locations.route("/add_location", methods=['GET','POST'])
def add_location():
    db.create_all()

    if current_user.is_authenticated:
        if (current_user.username == "kdm951027"):
            form = LocationForm()
            if form.validate_on_submit():
                location = Location(name=form.name.data)
                db.session.add(location)
                db.session.commit()
                flash('New Location Added in!','success')
                return redirect(url_for('main.home'))
            return render_template('add_location.html',title='Add Location', form=form)
        else:
            return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))

@locations.route("/add_seat", methods=['GET','POST'])
def add_seat():
    if current_user.is_authenticated:
        if (current_user.username == "kdm951027"):
            form = SeatForm()
            if form.validate_on_submit():
                location_id_from_name  = Location.query.filter_by(name=form.location_name.data).first()
                seat = Seat(location_name=form.location_name.data, col_num=form.col_num.data, \
                row_num=form.row_num.data, where=location_id_from_name)

                db.session.add(seat)
                db.session.commit()
                flash('New Seat is Added in!','success')
                return redirect(url_for('main.home'))
            return render_template('add_seat.html',title='Add Seat', form=form)
        else:
            return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))
