from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog.models import Location, Seat
from flaskblog import db
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.locations.forms import LocationForm, SeatForm, ReserveForm

locations = Blueprint('locations', __name__)

@locations.route("/add_location", methods=['GET','POST'])
def add_location():
    if current_user.is_authenticated:
        if (current_user.username == "admin"):
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

@locations.route("/add_seat/<string:locationName>", methods=['GET','POST'])
def add_seat(locationName):
    if current_user.is_authenticated:
        if (current_user.username == "admin"):
            form = SeatForm()
            location  = Location.query.filter_by(name=locationName).first_or_404()
            existing_seats = location.seats
            seat_nums = []
            seat_imgs =[]

            for seat in existing_seats:
                seat_nums.append(int(seat.seat_num))
                seat_imgs.append(int(seat.seat_img_id))

            if form.validate_on_submit():

                new_seats = form.seat_num.data.split(',')
                new_imgs = form.seat_img_ids.data.split(',')
                seat_len = len(new_seats)
                img_len = len(new_imgs)

                if (seat_len != img_len):
                    flash('Something went wrong when adding seat...!','danger')
                    return redirect(url_for('main.home'))

                for j in range(seat_len):
                    cur_seat = int(new_seats[j])
                    cur_img = int(new_imgs[j])
                    seat = Seat(location_name=locationName, seat_num=cur_seat, \
                    seat_img_id=cur_img,where=location)
                    db.session.add(seat)
                if seat:
                    db.session.commit()
                else:
                    db.session.rollback()

                flash('New Seat is Added in!','success')
                return redirect(url_for('main.home'))
            return render_template('add_seat.html',title='Add Seat', form=form, locationName=locationName,\
             existing_seats=existing_seats, seat_nums=seat_nums, seat_imgs=seat_imgs)
        else:
            return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))

@locations.route("/location/<string:name>")
def show_seats(name):
    location = Location.query.filter_by(name=name).first_or_404()
    seats = Seat.query.filter_by(where=location)
    seat_nums = []
    seat_imgs =[]
    for seat in seats:
        seat_nums.append(int(seat.seat_num))
        seat_imgs.append(int(seat.seat_img_id))
    return render_template('location.html',seats=seats,seat_nums=seat_nums,seat_imgs=seat_imgs,location=location)

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

@locations.route("/remove_location/<string:locationName>", methods=['GET','POST'])
@login_required
def remove_location(locationName):
    if current_user.is_authenticated:
        if (current_user.username == "admin"):
            location = Location.query.filter_by(name=locationName).first_or_404()
            location_id = location.id
            db.session.delete(location)
            db.session.commit()
            flash("You removed the location",'success')
            return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))
