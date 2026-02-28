from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import os

# --------------------
# App Config
# --------------------
app = Flask(__name__)
app.secret_key = "day8-secret-key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "food.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --------------------
# Models
# --------------------

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

    reviews = db.relationship(
        "Review",
        backref="restaurant",
        cascade="all, delete",
        lazy=True
    )

    def avg_rating(self):
        if not self.reviews:
            return None
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    reviews = db.relationship(
        "Review",
        backref="user",
        cascade="all, delete",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurant.id"),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

# --------------------
# Helper
# --------------------

def login_required():
    return "user_id" in session

# --------------------
# Routes
# --------------------

@app.route("/")
def home():
    return render_template("home.html")

# --------------------
# Restaurants
# --------------------

@app.route("/restaurants")
def restaurants():
    keyword = request.args.get("q")

    if keyword:
        restaurants = Restaurant.query.filter(
            Restaurant.name.contains(keyword)
        ).all()
    else:
        restaurants = (
            Restaurant.query
            .outerjoin(Review)
            .group_by(Restaurant.id)
            .order_by(func.count(Review.id).desc())
            .all()
        )

    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/restaurants/<int:id>")
def restaurant_detail(id):
    restaurant = Restaurant.query.get_or_404(id)
    return render_template("restaurant_detail.html", restaurant=restaurant)


@app.route("/add-restaurant", methods=["GET", "POST"])
def add_restaurant():
    if not login_required():
        flash("Please login first", "warning")
        return redirect("/login")

    if request.method == "POST":
        restaurant = Restaurant(
            name=request.form["name"],
            location=request.form["location"],
            description=request.form["description"]
        )
        db.session.add(restaurant)
        db.session.commit()

        flash("Restaurant added successfully!", "success")
        return redirect("/restaurants")

    return render_template("add_restaurant.html")


@app.route("/restaurants/<int:id>/review", methods=["POST"])
def add_review(id):
    if not login_required():
        flash("Please login first", "warning")
        return redirect("/login")

    rating = int(request.form["rating"])
    user_id = session["user_id"]

    review = Review.query.filter_by(
        restaurant_id=id,
        user_id=user_id
    ).first()

    if review:
        review.rating = rating
        flash("Review updated successfully", "success")
    else:
        review = Review(
            rating=rating,
            restaurant_id=id,
            user_id=user_id
        )
        db.session.add(review)
        flash("Review added successfully", "success")

    db.session.commit()
    return redirect(f"/restaurants/{id}")


@app.route("/restaurants/<int:id>/delete", methods=["POST"])
def delete_restaurant(id):
    if not login_required():
        flash("Please login first", "warning")
        return redirect("/login")

    restaurant = Restaurant.query.get_or_404(id)

    user_review = Review.query.filter_by(
        restaurant_id=id,
        user_id=session["user_id"]
    ).first()

    if not user_review:
        flash("You can delete only restaurants you reviewed", "danger")
        return redirect("/restaurants")

    db.session.delete(restaurant)
    db.session.commit()

    flash("Restaurant deleted", "danger")
    return redirect("/restaurants")

# --------------------
# My Reviews (FIXED)
# --------------------

@app.route("/my-reviews")
def my_reviews():
    if not login_required():
        flash("Please login first", "warning")
        return redirect("/login")

    reviews = (
        Review.query
        .join(Restaurant)
        .filter(Review.user_id == session["user_id"])
        .all()
    )

    return render_template("my_reviews.html", reviews=reviews)

# --------------------
# Auth
# --------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect("/register")

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Register success! Please login.", "success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"]
        ).first()

        if user and user.check_password(request.form["password"]):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login success", "success")
            return redirect("/restaurants")

        flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect("/")

# --------------------
# Run App
# --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)