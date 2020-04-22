from flask import render_template, url_for, flash, redirect, request
from . import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, AnnotationForm, EvalForm
from .models import User, Annotation, Eval, Ranking, fb_type
from flask_login import login_user, current_user, logout_user, login_required
from wtforms.validators import ValidationError
import sys
import random
import json
from sqlalchemy import exc

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:

        annotations_todo = Annotation.query.filter_by(user_id = int(current_user.get_id()), annotated=False).count()
        if annotations_todo > 0:
            return redirect(url_for('annotate'))
        else:
            return render_template('home.html', annotations_todo = 0)
        """
        evals_todo = Eval.query.filter_by(user_id = int(current_user.get_id()), evaled=False).count()"""
        return render_template('home.html', annotations_todo = annotations_todo)


    form = LoginForm()
    return render_template('home.html', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        empty_user = User.query.filter_by(registered=False).first()
        empty_user.username = form.username.data
        empty_user.email = form.email.data
        empty_user.password = hashed_password
        empty_user.native_language = form.native_language.data 
        empty_user.german_level = form.german_level.data 
        empty_user.english_level = form.english_level.data
        empty_user.registered = True
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('annotate'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html')


@app.route("/annotate", methods=['GET', 'POST'])
@login_required
def annotate():

    form = AnnotationForm()

    if form.validate_on_submit():
        key = int(form.key.data)
        toAnnotate = Annotation.query.filter_by(id=key).first()
        userChoice = None
        if form.userchoice.data == "marking":
            userChoice = fb_type.marking
        elif form.userchoice.data == "postedit":
            userChoice = fb_type.post_edit
        else:
            userChoice = toAnnotate.feedback_type
        toAnnotate.annotation = form.annotationfield.data
        toAnnotate.time_started = form.timestarted.data
        toAnnotate.time_submitted = form.timesubmitted.data
        toAnnotate.key_strokes = form.keystrokes.data
        toAnnotate.click_count = form.clicks.data
        toAnnotate.time_paused = form.timepaused.data
        toAnnotate.user_choice = userChoice
        toAnnotate.annotated = True
        db.session.commit()
        return redirect('/annotate')
    else:
        print(form.errors)


    nextAnnotate = Annotation.query.filter_by(
        user_id=current_user.id, annotated=False).order_by(Annotation.id).first()


    if nextAnnotate == None:
        return redirect('/home')

    target = nextAnnotate.target
    target = target.replace('"', '\\"')

    form.key.default = str(nextAnnotate.id)
    form.process()
    if nextAnnotate.feedback_type == fb_type.post_edit:
        instructions = "Please post-edit the translated sentence below with your improvements."
        return render_template('annotate.html', title='Annotate', instructions=instructions, source=nextAnnotate.src, target=target, form=form, fb_type="postedit")

    if nextAnnotate.feedback_type == fb_type.marking:
        instructions = "Please click or highlight incorrect words in the translated sentence below."
        return render_template('annotate.html', title='Annotate', instructions=instructions, source=nextAnnotate.src, target=target, form=form, fb_type="marking")
    instructions = """Please select either Post Edits or Markings.
        Post Edits: Edit the target sentence with your improvements.
        Markings: Mark incorrect words by clicking or highlighting."""
    return render_template('annotate.html', title='Annotate', instructions=instructions, source=nextAnnotate.src, target=target, form=form, fb_type="userchoice")


@app.route("/eval", methods=['GET', 'POST'])
@login_required
def eval():
    form = EvalForm()
    form.minimum = -1
    form.maximum = 2
    if form.validate_on_submit():
        toEval = Eval.query.filter_by(id=int(form.key.data)).first()
        toEval.better = form.better.data
        toEval.time_paused = form.timepaused.data
        toEval.time_started = form.timestarted.data
        toEval.time_submitted = form.timesubmitted.data
        toEval.click_count = form.clicks.data
        toEval.evaled = True
        db.session.commit()
        return redirect("/eval")

    nextEval = Eval.query.filter_by(user_id=current_user.id, evaled=False).first()

    if (nextEval == None):
        flash('There are currently no more evaluations for you at this moment.')
        return redirect('/home')
    target1 = nextEval.target1
    target2 = nextEval.target2
    src = nextEval.src
    target1.replace("'", "\'")
    target2.replace("'", "\'")
    choices = [['1', target1], ['2', target2]]
    random.shuffle(choices)
    choices.append(['-1', "No Preference"])
    form.key.default = int(nextEval.id)
    form.process()
    choice_json = json.dumps(choices)
    return render_template('eval.html', source=src, form=form, targets=choices, action="eval")

@app.route("/ranking", methods=['GET', 'POST'])
@login_required
def ranking():
    form = EvalForm()
    form.minimum = -1
    form.maximum = 5
    if form.validate_on_submit():
        toRank = Ranking.query.filter_by(id=int(form.key.data)).first()
        better = form.better.data
        toRank.time_paused = form.timepaused.data
        toRank.time_started = form.timestarted.data
        toRank.time_submitted = form.timesubmitted.data
        toRank.click_count = form.clicks.data
        toRank.ranking = str(better)
        toRank.ranked = True
        db.session.commit()
        return redirect("/ranking")

    nextRank = Ranking.query.filter_by(user_id=current_user.id, ranked=False).first()

    if (nextRank == None):
        flash('There are currently no more evaluations for you at this moment.')
        return redirect('/home')
    target1 = nextRank.target1
    target2 = nextRank.target2
    target3 = nextRank.target3
    target4 = nextRank.target4
    target5 = nextRank.target5

    src = nextRank.src
    target1.replace("'", "\\\'")
    target2.replace("'", "\\\'")
    target3.replace("'", "\\\'")
    target4.replace("'", "\\\'")
    target5.replace("'", "\\\'")
    form.key.default = int(nextRank.id)
    form.process()
    choices = [['1', target1], ['2', target2], ['3', target3], ['4', target4], ['5', target5]]
    random.shuffle(choices)
    choices.append(['-1', "No Preference"])

    choice_json = json.dumps(choices)
    return render_template('eval.html', source=src, form=form, targets=choices, action="ranking")

