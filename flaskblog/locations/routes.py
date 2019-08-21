from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog.models import Location, Seat
from flaskblog import db
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.locations.forms import LocationForm, SeatForm, ReserveForm

locations = Blueprint('locations', __name__)

@locations.route("/add_location", methods=['GET','POST'])
def add_location():
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
                seat = Seat(location_name=form.location_name.data, seat_num=form.seat_num.data, \
                where=location_id_from_name)

                db.session.add(seat)
                db.session.commit()
                flash('New Seat is Added in!','success')
                return redirect(url_for('main.home'))
            return render_template('add_seat.html',title='Add Seat', form=form)
        else:
            return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))

@locations.route("/location/<string:name>")
def show_seats(name):
    location = Location.query.filter_by(name=name).first_or_404()
    seats = Seat.query.filter_by(where=location)
    return render_template('location.html',seats=seats, location=location)

@locations.route("/reserve/<int:seat_id>/<string:location_name>", methods=['GET','POST'])
@login_required
def reserve(seat_id, location_name):
    if current_user.is_authenticated:
        form = ReserveForm()
        seat = Seat.query.filter_by(id=seat_id).first_or_404()
        if form.validate_on_submit():
            # seat = Seat.query.filter_by(id=seat_id)
            # seat.seated = current_user
            current_user.seat_id = seat.id
            db.session.commit()
            flash('Reserved!','success')
            return redirect(url_for('locations.show_seats', name=location_name))
        return render_template('reserve.html', seat_id = seat.id, title='Reserve Seat', form=form)
    else:
        return redirect(url_for('main.home'))


@locations.route("/leave/<int:seat_id>/<string:location_name>", methods=['GET','POST'])
@login_required
def leave(seat_id, location_name):
    if current_user.is_authenticated:
        seat = Seat.query.filter_by(id=seat_id).first_or_404()
        current_user.seat_id = None
        db.session.commit()
        flash('You left the seat','success')
        return redirect(url_for('locations.show_seats', name=location_name))
    return redirect(url_for('main.about'))
