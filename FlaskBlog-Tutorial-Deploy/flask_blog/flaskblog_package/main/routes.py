from flask import Blueprint, render_template, session, request
from models import Post
from markupsafe import escape

main = Blueprint('main', __name__)



@main.errorhandler(404)
def not_found(e):
    return render_template('http404.html')

@main.route('/ipc')
def ipc():
    return render_template('ipc_dashboard.html')

@main.route('/inspect')
def ipc_inspection():
    return render_template('ipc_inspection.html')

@main.route('/user/<username>/')
def user_detail(username):
    return escape(f"Username:{username}")

@main.route('/')
@main.route('/home')
def home():
    session.permanent = True
    page = request.args.get('page',1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=1)
    return render_template('home.html',post= post)
    # return f"{current_user.username}--{current_user.email}"
@main.route('/about')
def about():
    session.permanent = True
    return render_template('about.html')






