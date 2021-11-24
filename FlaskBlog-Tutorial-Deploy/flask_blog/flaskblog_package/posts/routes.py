from flask import  render_template, url_for, flash, redirect, session, request, abort
from flaskblog_package.forms   import (PostForm)
from flaskblog_package.models import User, Post  # after initializing the main(__name__) and db import from models
from flaskblog_package import app, db, csrf, login_manager, mail
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint

posts = Blueprint('posts', __name__)

@login_manager.user_loader
def user_loader(user_id):
    '''
    return the user object
    '''
    user_id = User.query.get(user_id)
    print(user_id,'uuuuuuuuiiiiidddddddddd')
    return user_id

@posts.route('/new_post', methods = ['GET', 'POST'])
# @login_required
@csrf.exempt
def new_post():
    form = PostForm()
    print(session,'sssssssssssssssss')
    
    # if form.validate_on_submit(): 
    if request.method == 'POST': 
        print(session,'sssssssssssssssss')
        # print(current_user,current_user.id,'(((((((((((((((((((((((')
        post = Post(title= form.title.data, content= form.content.data, user_id=current_user.id )
        print(post,'((2222222222222')

        db.session.add(post)
        db.session.commit()

        flash('Your Post has been created Successfully','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title= 'New Post', form= form, legend= 'Update Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title= post.title, post=post )

@posts.route('/post/<int:post_id>/update',methods = ['GET', 'POST'])
# @login_required
def update_post(post_id):
   
    post = Post.query.get_or_404(post_id)     
    
    # if post.author != current_user:
    #     abort(403)
    form = PostForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        post_obj = Post.query.get(post_id)
        # current_user  = User.query.filter_by(post=post_id)
        # current_user  = User.query.join('post.author').filter_by(id=post_id)
        print(session ,post_obj.user_id,'*****************')
        post_obj  = db.session.query(Post).filter_by(user_id= post_obj.user_id,id= post_id)
        post_obj.title = form.title.data
        post_obj.content = form.content
        print(post_obj.title,post_obj.content,'&&&&&&&&&&&&&&&&')
        db.session.commit()
        # print(post_obj, post_obj.title, post_obj.content,'&&&&&&&^^^^^^^^^^^')

        flash('Your Post has been updated successfully','success')
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title= post.title, form=form, legend= 'Update Post')

@posts.route('/post/<int:post_id>/delete',methods = ['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)     
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted successfully','success')
    return redirect(url_for('home'))
