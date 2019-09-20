from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from flask_login import current_user
from flaskblog.models import Location, Seat

class LocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

    def validate_name(self, name):
        location  = Location.query.filter_by(name=name.data).first()
        if location:
            raise ValidationError('That Location is already in DB')

    submit = SubmitField('Add')

class SeatForm(FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired(), Length(min=2, max=20)])
    # seat_num = IntegerField('Seat Number (1 ~ 20)', validators=[DataRequired(), NumberRange(min=1, max=20)])
    # changed to StringField since it comes in comma seperated values
    seat_num = StringField('Drag and Drop Seats from Above', validators=[DataRequired()])
    seat_img_ids = StringField('Seat Images are...',  validators=[DataRequired()])

    # def validate_location_name(self, location_name):
    #     location  = Location.query.filter_by(name=location_name.data).first()
    #     if not location:
    #         raise ValidationError('That Location is not in DB')

    def validate_seat_num(self, seat_num):
        for s_num in seat_num.data.split(','):
            try:
                int_s_num = int(s_num);
                if (int_s_num > 132 or int_s_num < 1):
                    raise ValidationError("That seat doesn't exist")
            except ValueError:
                raise ValidationError('Drag and Drop! or Numbers sperated by comma (1~132)')

    submit = SubmitField('Add')



class ReserveForm(FlaskForm):
    message = StringField('Message', validators=[Length(min=0, max=40)])
    submit = SubmitField('Reserve')
