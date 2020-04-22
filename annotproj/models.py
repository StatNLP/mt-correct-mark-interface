from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
import enum
import datetime

class fb_type(enum.Enum):
    post_edit = 1
    marking = 2
    user_decide = 3

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    registered = db.Column(db.Boolean, nullable=True, default=False)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=True)
    #posts = db.relationship('Post', backref='author', lazy=True)
    annot= db.relationship('Annotation', backref='author', lazy=True)

    native_language = db.Column(db.String(2), nullable=True)
    german_level = db.Column(db.String(10), nullable=True)
    english_level = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        #return f"User('{self.username}', '{self.email}')"
        return '<User {} {}>'.format(self.username, self.email)

    def get_id(self):
        return str(self.id) 


class Eval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    src = db.Column(db.Text, nullable=False)
    target1 = db.Column(db.Text, nullable=False)
    model1 = db.Column(db.Text, nullable=False)
    target2 = db.Column(db.Text, nullable=False)
    model2 = db.Column(db.Text, nullable=False)
    better = db.Column(db.Integer, nullable=True)
    evaled = db.Column(db.Boolean, nullable=True, default=False)
    time_started = db.Column(db.Integer, nullable=True)
    time_submitted = db.Column(db.Integer, nullable=True)
    time_paused = db.Column(db.Integer, nullable=True)
    click_count = db.Column(db.Integer, nullable=True)
    session = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now())


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    src = db.Column(db.Text, nullable=False)
    target1 = db.Column(db.Text, nullable=True)
    target2 = db.Column(db.Text, nullable=True)
    target3 = db.Column(db.Text, nullable=True)
    target4 = db.Column(db.Text, nullable=True)
    target5 = db.Column(db.Text, nullable=True)
    model1 = db.Column(db.Text, nullable=True)
    model2 = db.Column(db.Text, nullable=True)
    model3 = db.Column(db.Text, nullable=True)
    model4 = db.Column(db.Text, nullable=True)
    model5 = db.Column(db.Text, nullable=True)
    ranking = db.Column(db.Text, nullable=True)
    ranked = db.Column(db.Integer, nullable = True, default = False)
    time_started = db.Column(db.Integer, nullable=True)
    time_submitted = db.Column(db.Integer, nullable=True)
    time_paused = db.Column(db.Integer, nullable=True)
    click_count = db.Column(db.Integer, nullable=True)
    session = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now())


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src=db.Column(db.Text, nullable=False, default='')
    target = db.Column(db.Text, nullable=False, default='')
    feedback_type = db.Column(db.Enum(fb_type))
    user_choice = db.Column(db.Enum(fb_type))
    system_choice = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    annotation = db.Column(db.Text, nullable=True)
    is_train = db.Column(db.Boolean, nullable=True)
    annotated = db.Column(db.Boolean, nullable=True, default=False)
    key_strokes = db.Column(db.Integer, nullable=True, default=0)
    time_started = db.Column(db.Integer, nullable=True)
    time_submitted = db.Column(db.Integer, nullable=True)
    time_paused = db.Column(db.Integer, nullable=True)
    click_count = db.Column(db.Integer, nullable=True)
    session = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now())
    sentence_id = db.Column(db.Text, nullable=False, default='')
    agreement = db.Column(db.Boolean, nullable=True, default=False)

    def __repr__(self):
        return '<Annotation saved {}>'.format(self.src)
