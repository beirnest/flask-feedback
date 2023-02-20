from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, AddFeedbackForm

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def redirect_home():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_new_user():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.username

        return redirect(f"/users/{username}")

    else:
        return render_template(
            "register.html", form=form)
    
@app.route('/users/<username>')
def show_secret(username):
    if "user_id" not in session or session["user_id"] != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        u = User.query.filter_by(username=username).first()
        return render_template("secret.html", user=u)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete a user"""

    if "user_id" not in session or session["user_id"] != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()

    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Loads form to add feedback if user is logged in and then adds feedback to db. Redirects to userpage"""
    form = AddFeedbackForm()
    if "user_id" not in session or session["user_id"] != username:
            flash("You must be logged in to add feedback!")
            return redirect("/")
    else:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{username}")
        else:
            return render_template(
                "add_feedback.html", form=form)
        
@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """Loads form to add feedback if user is logged in and then adds feedback to db. Redirects to userpage"""
    form = AddFeedbackForm()
    feedback = Feedback.query.get_or_404(feedback_id)
    if "user_id" not in session or session["user_id"] != feedback.user.username:
            flash("You must be logged in to edit your feedback!")
            return redirect("/")
    else:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback.title = title
            feedback.content = content
            db.session.commit()
            return redirect(f"/users/{feedback.user.username}")
        else:
            return render_template(
                "edit_feedback.html", form=form, feedback=feedback)
        
@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """Delete a Feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if "user_id" not in session or session["user_id"] != feedback.user.username:
        flash("You must be logged in to delete your feedback!")
        return redirect("/")

    else:
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.user.username}")