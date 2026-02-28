from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

# --------------------
# App Configuration
# --------------------
app = Flask(__name__)
app.secret_key = "day8-secret-key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'food.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------
# Database Model
# --------------------
# --------------------
# Database Models
# --------------------

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

    reviews = db.relationship("Review", backref="restaurant", lazy=True)

    def avg_rating(self):
        if not self.reviews:
            return None
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurant.id"),
        nullable=False
    )

# --------------------
# Routes
# --------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# --------------------
# Restaurants
# --------------------

@app.route("/restaurants")
def restaurants():
    keyword = request.args.get("q")

    if keyword:
        data = Restaurant.query.filter(
            Restaurant.name.contains(keyword)
        ).all()
    else:
        data = Restaurant.query.all()

    return render_template("restaurants.html", restaurants=data)

@app.route("/add-restaurant", methods=["GET", "POST"])
def add_restaurant():
    if request.method == "POST":
        new_restaurant = Restaurant(
            name=request.form["name"],
            location=request.form["location"],
            description=request.form["description"]
        )
        db.session.add(new_restaurant)
        db.session.commit()

        flash("Restaurant added successfully!", "success")
        return redirect("/restaurants")

    return render_template("add_restaurant.html")

@app.route("/restaurants/<int:id>/edit", methods=["GET", "POST"])
def edit_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)

    if request.method == "POST":
        restaurant.name = request.form["name"]
        restaurant.location = request.form["location"]
        restaurant.description = request.form["description"]
        db.session.commit()

        flash("Restaurant updated successfully!", "warning")
        return redirect("/restaurants")

    return render_template("edit_restaurant.html", restaurant=restaurant)

# 🔒 DELETE using POST (COMMIT 3)
@app.route("/restaurants/<int:id>/delete", methods=["POST"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()

    flash("Restaurant deleted successfully!", "danger")
    return redirect("/restaurants")

# --------------------
# Run App
# --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)