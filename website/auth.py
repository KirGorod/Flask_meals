from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)




@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.admin"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
               login_user(user=user, remember=True) 
               return redirect(url_for("views.admin"))
        else:
            print("USER DOES NOT EXIST!!!")
            
    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            print("Email is already taken")
        elif len(email) < 4:
            print("Email must be greater than 4 characters")
        elif password1 != password2:
            print("Passwords do not match!")
        elif len(password1) < 6:
            print("Password to short!")
        else:
            new_user = User(email = email, password = password1)
            db.session.add(new_user)
            db.session.commit()
            print("USER CREATED!")

            return redirect(url_for("views.index"))

    return render_template("register.html")