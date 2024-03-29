from enum import Enum
from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, redirect, request


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.url)

class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class hobbyType(ExtendedEnum):
    outdoor = "outdoor"
    indoor = "indoor"
    game = "game"
    course = "course"

class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(hobbyType))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Hobby('{self.name}','{self.type}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    hobbies = db.relationship('Hobby', backref='hobbier', lazy=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    seats = db.relationship('Seat',cascade="all,delete,delete-orphan", backref='where')

    def __repr__(self):
        return f"Location('{self.name}','{self.image_file}')"

class Seat(db.Model):
    __table_args__ = (
        db.UniqueConstraint('location_name', 'seat_num', name='unique_seat_info'),
    )

    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    seat_num = db.Column(db.Integer, nullable=False)
    seat_img_id = db.Column(db.Integer, nullable=False)
    users = db.relationship('User', backref='seated', lazy=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __repr__(self):
        return f"Seat('{self.location_name}', '{self.seat_num}')"


# def _create_database():
#     """
#     If this script is run directly, create all the tables necessary to run the
#     application.
#     """
#     app = Flask(__name__)
#     app.config.from_pyfile('./config.py')
#     init_app(app)
#     with app.app_context():
#         db.create_all()
#     print("All tables created")
#
# if __name__ == '__main__':
#     _create_database()
