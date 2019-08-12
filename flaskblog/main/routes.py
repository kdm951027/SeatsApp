from flask import Blueprint, render_template, request
from flaskblog.models import Post, Location

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    locations = Location.query.all()
    return render_template('home.html', posts=posts, locations=locations)

@main.route("/about")
def about():
    return render_template('about.html',title='About')
