import datetime

from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
import secrets
import os
from PIL import Image
from flaskblog.db import add_post
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from .models import Post, User
from . import mysql, bcrypt, login_manager
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    return User(**user) if user else None

@bp.route("/")
@bp.route("/home")
def home():
    cur= mysql.connection.cursor()
    cur.execute("SELECT * FROM post")
    posts = cur.fetchall()
    cur.close()
    return render_template('home.html', posts=posts)  # fixed: template file is home.html, not main.home.html


@bp.route("/about")
def about():
    return render_template('about.html', title='About')  # fixed: was main.about.html

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = (form.username.data,form.email.data, hashed_password)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", (user[0], user[1], user[2]))    
        mysql.connection.commit()
        cur.close()
        flash(f'Your account has been created, you are now able to log in!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)  

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))   
    form = LoginForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s", (form.email.data,))
        row = cur.fetchone()
        cur.close()
        if row and bcrypt.check_password_hash(row['password'], form.password.data):
            user = User(**row)
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO post (title, content, date_posted, user_id) VALUES (%s, %s, %s, %s)", (form.title.data, form.content.data, datetime.now(), current_user.id))
        mysql.connection.commit()
        cur.close()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='New Post')

@bp.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return 'img/' + picture_fn

@bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE user SET username = %s, email = %s, image_file = %s WHERE user_id = %s",
            (current_user.username, current_user.email, current_user.image_file, current_user.id)
        )
        mysql.connection.commit()
        cur.close()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for('static', filename=current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
