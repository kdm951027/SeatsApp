from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms import StringField, SubmitField, IntegerField
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
    col_num = IntegerField('Column Number (1 ~ 12)', validators=[DataRequired(), NumberRange(min=1, max=12)])
    row_num = IntegerField('Row Number (1 ~ 12)', validators=[DataRequired(), NumberRange(min=1, max=12)])

    def validate_location_name(self, location_name):
        location  = Location.query.filter_by(name=location_name.data).first()
        if not location:
            raise ValidationError('That Location is not in DB')
        # else:
        #     seat_location = Seat.query.filter_by(location_name=location_name.data).first()
        #     if seat_location:
        #         col  = Seat.query.filter_by(col_num=col_num.data).first()
        #         if col:
        #             row = Seat.query.filter_by(row_num=row_num.data).first()
        #             if row:
        #                 raise ValidationError('That Seat is already in DB')

    submit = SubmitField('Add')
