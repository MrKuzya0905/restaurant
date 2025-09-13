from flask_wtf import FlaskForm
import wtforms 

class SignUpForm(FlaskForm):
    username = wtforms.StringField(
        label='login',
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=4)]
    )
    first_name = wtforms.StringField(label='first name(optional)')
    last_name = wtforms.StringField(label='last name(optional)')
    password = wtforms.PasswordField(
        label='password',
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=6)]
    )
    submit = wtforms.SubmitField(label='Sign Up')

class SignInForm(FlaskForm):
    username = wtforms.StringField(
        label='login',
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=4)]
    )
    password = wtforms.PasswordField(
        label='password',
        validators=[wtforms.validators.DataRequired(), wtforms.validators.Length(min=6)]
    )
    submit = wtforms.SubmitField(label='Sign In')

class OrderForm(FlaskForm):
    name = wtforms.SelectField(label='Dish name', validators=[wtforms.validators.DataRequired()])
    count = wtforms.IntegerField(label='Count', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField(label='Order')

class ReservationForm(FlaskForm):
    timestamp = wtforms.DateTimeField(label='Date and time', validators=[wtforms.validators.DataRequired()])
    table_number = wtforms.IntegerField(label='Table number', validators=[wtforms.validators.DataRequired()])
    numbers = wtforms.IntegerField(
        label='Number of people',
        validators=[wtforms.validators.NumberRange(min=1), wtforms.validators.DataRequired()]
    )
    submit = wtforms.SubmitField(label='Reserve')