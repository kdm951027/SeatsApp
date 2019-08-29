from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
RequestResetForm, ResetPasswordForm, UpdateHobbyForm)
from flaskblog.models import User, Post, Location, Hobby, hobbyType
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can log in now','success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title = 'Register', form=form)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # return redirect(url_for(next_page)) if next_page else redirect(url_for('main.home'))
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/update_hobby", methods=['GET','POST'])
@login_required
def update_hobby():
    form = UpdateHobbyForm()
    if form.validate_on_submit():
        hobby = Hobby(name=form.name.data, type=form.type.data, hobbier=current_user)
        db.session.add(hobby)
        db.session.commit()
        flash('New hobby has been updated!', 'success')
        return redirect(url_for('users.account'))
    return render_template('update_hobby.html', title='Update Hobby', form=form)

@users.route("/update_hobby/<int:hobby_id>/delete", methods=['GET','POST'])
@login_required
def delete_hobby(hobby_id):
    hobby = Hobby.query.get_or_404(hobby_id)
    if hobby.hobbier != current_user:
        abort(403)
    db.session.delete(hobby)
    db.session.commit()
    flash('Your Hobby has been removed.', 'success')
    return redirect(url_for('users.update_hobby'))


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())\
    .paginate(page=page,per_page=2)
    return render_template('user_posts.html',posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password', form=form)

@users.route("/profile/<string:username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
