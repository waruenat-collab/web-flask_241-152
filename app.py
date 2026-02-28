from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import os

app = Flask(__name__)
app.secret_key = "day8-secret-key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "food.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------- Models --------------------

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

    reviews = db.relationship("Review", backref="restaurant", cascade="all, delete")

    def avg_rating(self):
        if not self.reviews:
            return None
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    reviews = db.relationship("Review", backref="user", cascade="all, delete")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# -------------------- Helper --------------------

def login_required():
    return "user_id" in session

# -------------------- Routes --------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/restaurants")
def restaurants():
    keyword = request.args.get("q")
    if keyword:
        data = Restaurant.query.filter(Restaurant.name.contains(keyword)).all()
    else:
        data = (
            Restaurant.query
            .outerjoin(Review)
            .group_by(Restaurant.id)
            .order_by(func.count(Review.id).desc())
            .all()
        )
    return render_template("restaurants.html", restaurants=data)

@app.route("/restaurants/<int:id>")
def restaurant_detail(id):
    restaurant = Restaurant.query.get_or_404(id)
    return render_template("restaurant_detail.html", restaurant=restaurant)

@app.route("/add-restaurant", methods=["GET", "POST"])
def add_restaurant():
    if not login_required():
        return redirect("/login")

    if request.method == "POST":
        r = Restaurant(
            name=request.form["name"],
            location=request.form["location"],
            description=request.form["description"]
        )
        db.session.add(r)
        db.session.commit()
        return redirect("/restaurants")

    return render_template("add_restaurant.html")

@app.route("/restaurants/<int:id>/review", methods=["POST"])
def add_review(id):
    if not login_required():
        return redirect("/login")

    rating = int(request.form["rating"])
    user_id = session["user_id"]

    review = Review.query.filter_by(
        restaurant_id=id,
        user_id=user_id
    ).first()

    if review:
        review.rating = rating
    else:
        review = Review(
            rating=rating,
            restaurant_id=id,
            user_id=user_id
        )
        db.session.add(review)

    db.session.commit()
    return redirect(f"/restaurants/{id}")

@app.route("/my-reviews")
def my_reviews():
    if not login_required():
        return redirect("/login")

    reviews = Review.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template("my_reviews.html", reviews=reviews)

# -------------------- Auth --------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form["username"])
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.check_password(request.form["password"]):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/restaurants")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------------------- Run --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)