from flask import render_template, url_for, flash, redirect, request, session
from bookmyrepair import app, db , bcrypt
from bookmyrepair.forms import RegistrationForm, LoginForm
from bookmyrepair.models import User
from flask_login import login_user, current_user, logout_user, login_required
import os
from bookmyrepair.products.models import Addservice, Category


@app.route("/Home")
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method=='POST'  and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('SignUp.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method =='POST' and form.validate_on_submit():
        if form.email.data=='admin@gmail.com' and form.password.data=='admin':
            session['email'] = form.email.data
            return redirect(url_for('adminhome'))
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('custhome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/Custhome")
@login_required
def custhome():
    return render_template('Custhome.html')


@app.route("/Adminhome")
def adminhome():
    services = Addservice.query.all()
    return render_template('Adminhome.html', services=services)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/categories")
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('Category.html',categories=categories)

@app.route("/About")
def about():
    return render_template('about.html')

@app.route("/Contact")
def contact():
    return render_template('contact.html')
