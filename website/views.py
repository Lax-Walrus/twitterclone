
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Chirps, User, Comment, Like
from . import db


views = Blueprint("views", __name__)

#  home route shows all post and requires a user login


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Chirps.query.all()
    return render_template("home.html",  user=current_user, chirps=posts)

# create chirp/post route requires user login


@views.route("/createchirp", methods=["GET", "POST"])
@login_required
def createPost():
    # checks the createchirps.form if text is empty throws error
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash("Post cannot be empty", category="error")
        # adds chirp/post to the database
        else:
            post = Chirps(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Posted Chirp succesfully", category="success")
            return redirect(url_for("views.home"))
    return render_template('createchirp.html', user=current_user)

# delete chirp route requires user login


@views.route("/deletechirp/<id>")
@login_required
def deletechirp(id):
    # grabs the chirp/post from the database that matches the id of of the chirp by passing the id from the home.html or chrips.html
    post = Chirps.query.filter_by(id=id).first()

    # checks if the chirp/post exisists and if the user matches id matches the post author
    if not post:
        flash("Chirp does not exisit", category="error")

    elif current_user.id != post.author:
        flash("this is not your chirp to delete", category="error")

    else:
        db.session.delete(post)
        db.session.commit()
        flash("Chrip Deleted", category="success")

    return redirect(url_for("views.home"))

# profile page


@views.route('/chirps/<username>')
@login_required
def profiles(username):
    user = User.query.filter_by(username=username).first()
    # looks if user exists
    if not user:
        flash("no user found", category="error")
        return redirect(url_for("views.home"))

    posts = user.chirps
    # passes the data to chirps.html to loop through and display
    return render_template('chirps.html', user=current_user, chirps=posts, username=username)

# dashboard route


@views.route('/dashboard')
@login_required
def admindashboard():
    # checks if user is admin and shows if true
    if current_user == "admin":

        clients = User.query.all()
        return render_template('dashboard.html', users=clients)
    # redirects user to home if not admin
    else:
        flash("non-admin accounts cannot view this page", category="error")
        return redirect(url_for("views.home"))


# createcomment route
@views.route('/createcomment/<chirps_id>', methods=["POST"])
@login_required
def createcomment(chirps_id):
    text = request.form.get("text")
    # checks in comment form if there is data chripdiv.html
    if not text:
        flash("comment cannot be empty!", category="error")

    # adds the comment to the comment to the post if the post is found in the database
    else:
        post = Chirps.query.filter_by(id=chirps_id)

        if post:
            comment = Comment(
                text=text, author=current_user.id, chirp_id=chirps_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment added successfully", category="success")
        # lets user know post doesn't exist
        else:
            flash("Post doesn't exist", category="error")

    return redirect(url_for("views.home"))


# delete comment route
@views.route("/deletecomment/<comment_id>")
@login_required
def deletecomment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("Comment does not exist", category="error")

    elif current_user.id != comment.author and current_user.id != comment.chirp.author:
        flash("this is not your comment to delete", category="error")

    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment successfully removed!", category="success")

    return redirect(url_for("views.home"))


@views.route('/likechirp/<chirp_id>', methods=["POST"])
@login_required
def like(chirp_id):
    post = Chirps.query.filter_by(id=chirp_id).first()
    like = Like.query.filter_by(
        author=current_user.id, chirp_id=chirp_id).first()

    if not post:
        return jsonify({"error": "Post does not exist"}, 400)

    elif like:
        db.session.delete(like)
        db.session.commit()

    else:
        like = Like(author=current_user.id, chirp_id=chirp_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.like), "liked": current_user.id in map(lambda x: x.author, post.like)})
