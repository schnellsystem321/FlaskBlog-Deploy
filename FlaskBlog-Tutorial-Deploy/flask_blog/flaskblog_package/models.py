from flaskblog_package.__init__ import db 
from datetime import datetime
from flask_login import UserMixin
from itsdangerous.jws import TimedJSONWebSignatureSerializer as Serailizer 
from flaskblog_package import app
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(id= user_id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    image_field  = db.Column(db.String(20), nullable=False, default='../static/profile_pic/myprofile.png')
    password = db.Column(db.String(60),nullable= False)

    def get_reset_token(self, expires_in = 1800):
        s = Serailizer(app.config['SECRET_KEY'],expires_in)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serailizer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self) -> str:
        return f"User('{self.username}'{self.email})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable= False)
    date_posted = db.Column(db.DateTime, nullable= False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

    def __repr__(self) -> str:
        return f"Post('{self.title}'{self.date_posted}'"
    
def init_db():
    
    db.create_all()
    # Create a test user
    new_user = User()
    # new_user = User('Nathan','Nathan@email.com', 'Nathan')
    new_user.username = 'Nathan new1'
    new_user.email = 'Nathannew11@email.com'
    new_user.password = 'Nathan'
    db.session.add(new_user)
    db.session.commit()



# if __name__ == '__main__':
#     init_db()