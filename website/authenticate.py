from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# user authentication and checks for login/signup/admin etc

authenticate = Blueprint("authenticate", __name__)

# updated route


@authenticate.route("/updateUser/<username>", methods=["POST", "GET"])
@login_required
def userupdate(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("no user found", category="error")
        return redirect(url_for("views.home"))

    else:

        newusername = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        usernameexsits = User.query.filter_by(username=newusername).first()

        if usernameexsits:
            flash("username already taken", category="error")
            return redirect(url_for("views.chirps"))

        elif password1 != password2:
            flash('passwords do not match', category="error")
            return redirect(url_for("views.chirps"))
        elif len(newusername) < 2:
            flash("username is too short", category="error")
            return redirect(url_for("views.chirps"))
        elif len(password1) < 6:
            flash("password is too short", category="error")
            return redirect(url_for("views.chirps"))
        else:
            user.username = newusername
            user.password = generate_password_hash(
                password1, method='sha256')
            db.session.commit()
            flash("updated account successfully", category="success")
            return redirect(url_for('views.home'))

# login route


@authenticate.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # grabs email and password from the login html
        email = request.form.get("email")
        password = request.form.get("password")
        # searches the User database looking for the emails to matcch what was entered and return the first match
        user = User.query.filter_by(email=email).first()
        # checks if user was found and then pulls the hashed password to see if it matches the hashed password that was entered
        if user:
            if check_password_hash(user.password, password):
                flash("logged in", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            #  if password or email is wrong / not found lets user know one of them was incorrect
            else:
                flash("email or password is incorrect", category="error")
        else:
            flash("email or password is incorrect", category="error")

    return render_template("login.html", user=current_user)

# logout route this route requires user to be logged in


@authenticate.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


# sign up route


@authenticate.route("/signup", methods=["GET", "POST"])
def signup():
    # if post method  grabs the user entered data from the signup.html form
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # checks if the email and username entered match enteries in the database already

        emailexists = User.query.filter_by(email=email).first()
        usernameexists = User.query.filter_by(username=username).first()

        # if chain to let user know if password is to short, email or username already in use or if the passwords do not match

        if emailexists:
            flash('email already exists', category="error")
        elif usernameexists:
            flash('username has already been taken', category="error")
        elif password1 != password2:
            flash('passwords do not match', category="error")
        elif len(username) < 2:
            flash("username is too short", category="error")
        elif len(password1) < 6:
            flash("password is too short", category="error")

            # if all requirements are met creates a new user and hashes the user password before being stored in the database adds the user to the data base and logs them in automatically.
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Created', category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)

#  route used to create admin account


@authenticate.route("/createadmin", methods=["POST", "GET"])
def createAdmin():

    # if admin already exists will not let another one be created
    usernameexists = User.query.filter_by(isAdmin=True).first()

    if usernameexists:
        flash("admin already exsists", category="error")
        return redirect(url_for("views.home"))

    # creates a custom user where admin has admin boolean set to true. this boolean allows the admin to view the dashboard option on the navbar
    else:
        admin = User(email="admin@admin.com", username="admin",
                     password=generate_password_hash("password", method='sha256'), isAdmin=True)
        db.session.add(admin)
        db.session.commit()
        db.session.add(admin)
        db.session.commit()
        flash("admin created", category="success")
        return redirect(url_for("views.home"))
