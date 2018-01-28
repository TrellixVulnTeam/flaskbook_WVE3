from flask import Blueprint,render_template,request,redirect,session
from user.forms import RegisterForm,LoginForm
from wtforms.validators import ValidationError
import bcrypt

from user.models import User


user_app = Blueprint('user_app',__name__)


    
@user_app.route('/register',methods=('POST','GET'))
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        salt=bcrypt.gensalt(10)
        hashed_password=bcrypt.hashpw(form.password.data,salt)
        user = User(username=form.username.data,password=hashed_password,email=form.email.data,first_name=form.first_name.data,last_name=form.last_name.data)
        user.save()
        return 'User registered'
    return render_template('user/register.html',form=form)

def validate_username(form,field):
    if User.objects.filter(username=field.data).first():
        raise ValidationError("username already exists")
def validate_email(form,field):
    if User.objects.filter(email=field.data).first():
        raise ValidationError("email already taken")
@user_app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    
    
    if form.validate_on_submit():
        user = User.objects.filter(
            username=form.username.data
            ).first()
        if user:
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                session['username'] = form.username.data
                
            else:
                user = None
        if not user:
            error = 'Incorrect credentials'
    return render_template('user/login.html', form=form, error=error)
    
        



    
