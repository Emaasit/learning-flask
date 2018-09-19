# The authentication blueprint will have views to register new users and to log in and log out.

# A view function is the code you write to respond to requests to your application.
# Flask uses patterns to match the incoming request URL to the view that should handle it.
# The view returns data that Flask turns into an outgoing response. Flask can also go
# the other direction and generate a URL to a view based on its name and arguments.
#
# A Blueprint is a way to organize a group of related views and other code.
# Rather than registering views and other code directly with an application,
# they are registered with a blueprint. Then the blueprint is registered with
# the application when it is available in the factory function.
#
# Flaskr will have two blueprints, one for authentication functions and
# one for the blog posts functions. The code for each blueprint will go in a separate module.
# Since the blog needs to know about authentication, you’ll write the authentication one first.

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

# Create the authentication blueprint
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    The register view function
    :return:
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif db.execute(
                "SELECT id FROM user WHERE username = ?", username
        ).fetchone() is not None:    # Returns one row from the query
            error = "User {} is already registered".format(username)

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                username, generate_password_hash(password))
            db.commit()       # Save the changes since data is modified
            return redirect(url_for("auth.register"))

        # If validation fails, the error is shown to the user.
        # flash() stores messages that can be retrieved when rendering the template.
        flash(error)

    return render_template("auth/register.html")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
