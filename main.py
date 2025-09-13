from typing import List, Optional

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from models import db, User, Menu, Order, Reservation
from forms import SignUpForm, SignInForm, OrderForm, ReservationForm

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_message = "Please log in to access this page."
login_manager.login_view = 'sign_in'


# with app.app_context():
#     db.drop_all()
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


app.post('/sign-up/')
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed up! Please log in.', 'success')
        return redirect(url_for('sign_in'))
    
    return render_template('sign_up.html', form=form)


@app.post('/sign-in/')
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(username=form.username.data).first()
        if not user or not user.is_verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('sign_in'))
        
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('menu'))
    
    return render_template('sign_in.html', form=form)


@app.get('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')


@app.get('/')
def index():
    return render_template('index.html')

@app.get('/menu/')
def get_menu():
    menu = Menu.query.all()
    form = OrderForm()
    form.choices = [item.name for item in menu]
    return render_template('menu.html', menu=menu, form=form)