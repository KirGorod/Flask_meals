from flask import Blueprint, render_template, request, redirect, url_for
from . import db, allowed_file, create_app
from .models import Meals
from flask_login import login_required
from werkzeug.utils import secure_filename
import os


views = Blueprint("views", __name__)
app = create_app()

@views.route("/")
def index():
    meals = Meals.query.all()
    return render_template("index.html", meals=meals)


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == 'POST':
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        text = request.form.get("text")
        if 'file' not in request.files:
            return 'there is no file in form!'
        file = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        image = file.filename
        file.save(path)

        new_meal = Meals(title=title, subtitle=subtitle, text=text, image=image)
        db.session.add(new_meal)
        db.session.commit()
        print("Meal added")
        return redirect(url_for("views.index"))
    return render_template("admin.html")