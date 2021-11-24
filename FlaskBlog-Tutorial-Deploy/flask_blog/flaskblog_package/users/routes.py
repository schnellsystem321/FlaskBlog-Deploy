from flask import Blueprint
from math import pi, remainder
from operator import pos
from flask import  render_template, url_for, flash, redirect, session, request, abort
from flask_blog.flaskblog_package.users.forms import RequestResetForm, ResetPasswordForm
from flaskblog_package.users.forms   import (RegistrationForm, LoginForm, UpdateAccountForm,
                    RequestResetForm, ResetPasswordForm)
from flaskblog_package.models import User, Post  # after initializing the main(__name__) and db import from models
from flaskblog_package import app, db, csrf, login_manager, mail
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flaskblog_package.users.utils import save_picture,send_reset_email
bcrypt_pass = Bcrypt()

users = Blueprint('users',__name__)

@users.route('/register', methods =['GET', 'POST'])
@csrf.exempt # make wtf_csrf_enabled = false in app.config 
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RegistrationForm() # form is an instance of RegistrationForm class
    if form.validate_on_submit():
    # if request.method == 'POST':
        hashed_password = bcrypt_pass.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account created , Now You can login','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form =form)


@login_manager.user_loader
def user_loader(user_id):
    '''
    return the user object
    '''
    user_id = User.query.get(user_id)
    print(user_id,'uuuuuuuuiiiiidddddddddd')
    return user_id

@users.route('/login', methods =['GET', 'POST'])
@csrf.exempt
def login():
    session.permanent = True
    # current_user = None
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()   
    if form.validate_on_submit():
    #     session['email'] = request.form['email']

    # if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()
        session['email'] = request.form['email']       
        session['_user_id']  = user.id
        session['username']  = user.username
    
        if user and bcrypt_pass.check_password_hash(user.password,form.password.data):
            # active = login_user(user, remember =form.remember.data) #TypeError: login() takes 0 positional arguments but 1 was given
            active =login_user(user =user,remember=form.remember.data)
            next_page = request.args.get('next')
            # if next_page != None:
                # next_page = re.sub('/','',next_page)
            # return redirect(url_for(next_page))  if next_page  else redirect(url_for('home'))
            print(session,active,'&***************',next_page)
            return redirect(f'{next_page}')  if next_page  else redirect(url_for('home'))
        else:
            flash(f'login Unsuccessfull.Please check username and password','danger')
    
    # return render_template('login.html', title='Login', form= form)
    return render_template('login.html', title='Login', form= form)

@users.route('/logout')
def logout():
    logout_user()
    session.pop('email',None)
    return redirect(url_for('home'))



@users.route('/account', methods = ['GET', 'POST'])
@login_required
@csrf.exempt
def account():
    # current_user = User.query.filter_by(email='admin@email.com').first()
    
    # image_file =  url_for('static', filename= 'profile_pic'+ current_user.image_file)
    # image_file =  url_for('static', filename= 'profile_pic/profile.png')
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='/profile_pics/myprofile.png' )
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@users.route('/user/<string:username>', methods = ['GET'])
def user_post(username):
    session.permanent = True
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username= username).first_or_404()
    post = Post.query.filter_by(author=user)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page,per_page=2)
    

    return render_template('user_posts.html',post= post, user=user)
    # return f"{current_user.username}--{current_user.email}"


@users.route('/reset_password', methods = ['GET', 'POST'])
# @login_required
@csrf.exempt
def reset_request():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        user = User.query.filter_by(email= form.email.data).first()
        send_reset_email(user)
        flash('A email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('login'))
        
    return render_template('reset_request.html',title='Reset password',form=form)
    
@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # if request.method == 'POST':
        hashed_password = bcrypt_pass.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated , Now You can login','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset password',form=form)
    

