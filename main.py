from typing import List, Optional

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import db, User, Menu, Order, Reservation, OrderItem
from forms import SignUpForm, SignInForm, OrderForm, ReservationForm
from config import settings

app = Flask(__name__)
app.secret_key = settings.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_uri
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_message = "Please log in to access this page."
login_manager.login_view = 'sign_in'

def create_menu():
    if not Menu.query.first():
        dishes = [
            Menu(name="Pizza Margherita", ingredients="Tomato, Mozzarella, Basil", price=8.5),
            Menu(name="Caesar Salad", ingredients="Lettuce, Chicken, Croutons, Caesar dressing", price=6.0),
            Menu(name="Spaghetti Carbonara", ingredients="Spaghetti, Eggs, Pancetta, Parmesan", price=9.0)
        ]
        db.session.add_all(dishes)
        db.session.commit()
        print("Initial menu created.")

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     create_menu()
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/sign_up/', methods=['GET', 'POST'])
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
        flash('You have successfully signed up! Please log in.')
        return redirect(url_for('sign_in'))
    
    return render_template('sign_up.html', form=form)


@app.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(username=form.username.data).first()
        if not user or not user.is_verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('sign_in'))
        
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('index'))
    
    return render_template('sign_in.html', form=form)


@app.get('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.get('/')
def index():
    return render_template('index.html')

@app.route('/menu/', methods=['GET', 'POST'])
@login_required
def get_menu():
    menu = Menu.query.all()
    if request.method == 'POST':
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.flush()

        for item in menu:
            count = request.form.get(f"count_{item.id}")
            if count and count.isdigit() and int(count) > 0:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_id=item.id,
                    count=int(count)
                )
                db.session.add(order_item)

        db.session.commit()
        flash("Замовлення створене!")
        return redirect(url_for("index"))

    return render_template("menu.html", menu=menu)


@app.route('/reservation/', methods=['GET', 'POST'])
@login_required
def reservation():
    form = ReservationForm()
    if form.validate_on_submit():
        exists = Reservation.query.filter_by(
            table_number=form.table_number.data,
            timestamp=form.timestamp.data
        ).first()

        if exists:
            flash('This table is already reserved at the selected time. Please choose a different table or time.', 'danger')
            return redirect(url_for('reservation'))
        else:
            reservation = Reservation(
                timestamp=form.timestamp.data,
                table_number=form.table_number.data,
                numbers=form.numbers.data,
                user_id=current_user.id
            )
            db.session.add(reservation)
            db.session.commit()
            flash('Your reservation has been made successfully!', 'success')
            return redirect(url_for('index'))
    
    return render_template('reservation.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)